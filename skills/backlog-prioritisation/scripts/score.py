#!/usr/bin/env python3
"""Rank backlog items by RICE or WSJF.

CSV columns
  rice: id,name,reach,impact,confidence,effort      (confidence 0-1)
  wsjf: id,name,business_value,time_criticality,risk_reduction,job_size
  moscow: id,name,moscow,effort   (moscow = must/should/could/wont)
Usage: score.py rice|wsjf|moscow items.csv [--top N]
"""
import csv
import sys


def rice(r):
    return float(r["reach"]) * float(r["impact"]) * float(r["confidence"]) / float(r["effort"])


def wsjf(r):
    top = float(r["business_value"]) + float(r["time_criticality"]) + float(r["risk_reduction"])
    return top / float(r["job_size"])


METHODS = {"rice": rice, "wsjf": wsjf}


def rank(method, rows):
    scored = []
    for r in rows:
        try:
            s = METHODS[method](r)
        except ZeroDivisionError:
            raise ValueError(f"{r.get('id')}: effort or size is zero")
        scored.append({**r, "score": round(s, 2)})
    return sorted(scored, key=lambda r: -r["score"])


def ties(ranked, within=0.10):
    """Neighbours whose scores are within 10%: the model cannot tell them apart, so decide on dependencies."""
    out = []
    for a, b in zip(ranked, ranked[1:]):
        hi, lo = a["score"], b["score"]
        if hi > 0 and (hi - lo) / hi <= within:
            out.append((a["id"], b["id"]))
    return out


def moscow(rows):
    """Share of effort in each bucket. Musts above 60% leave no room to cope with surprises."""
    totals = {"must": 0.0, "should": 0.0, "could": 0.0, "wont": 0.0}
    for r in rows:
        key = r["moscow"].strip().lower().replace("'", "").replace("won't", "wont")
        if key not in totals:
            raise ValueError(f"{r.get('id')}: moscow must be must/should/could/wont, got '{r['moscow']}'")
        totals[key] += float(r["effort"])
    planned = totals["must"] + totals["should"] + totals["could"]
    shares = {k: (round(v / planned, 3) if planned else 0.0) for k, v in totals.items() if k != "wont"}
    warnings = []
    if shares["must"] > 0.6:
        warnings.append(f"Musts are {shares['must']:.0%} of planned effort (keep under 60%): too much is 'must', or the plan has no slack")
    if planned and shares["must"] == 0:
        warnings.append("nothing is a Must: is anything really needed?")
    return shares, warnings


if __name__ == "__main__":
    method, path = sys.argv[1], sys.argv[2]
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if method == "moscow":
        shares, warns = moscow(rows)
        print("Share of planned effort: " + ", ".join(f"{k} {v:.0%}" for k, v in shares.items()))
        for w in warns:
            print("WARNING: " + w)
        sys.exit(1 if warns else 0)
    ranked = rank(method, rows)
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else len(ranked)
    for i, r in enumerate(ranked[:top], 1):
        print(f"{i}. {r['id']}  {r['name']}  score={r['score']}")
    for a, b in ties(ranked[:top + 1]):
        print(f"Tie: {a} and {b} are within 10%: choose by dependencies and risk, not by the score")

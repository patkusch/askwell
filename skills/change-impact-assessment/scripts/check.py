#!/usr/bin/env python3
"""Check a people-side change impact table and show who needs attention first.

CSV columns: group,what_changes,rating,communication,training,support,readiness,owner
rating: high|medium|low   readiness: high|medium|low|unknown (how ready they are now)
"""
import csv
import sys

LEVEL = {"high": 3, "medium": 2, "low": 1}


def check(rows):
    out = []
    seen = set()
    for r in rows:
        g = (r.get("group") or "").strip()
        if not g:
            out.append("a row has no group")
            continue
        if g.lower() in seen:
            out.append(f"{g}: listed twice")
        seen.add(g.lower())
        rating = (r.get("rating") or "").strip().lower()
        ready = (r.get("readiness") or "").strip().lower()
        if rating not in LEVEL:
            out.append(f"{g}: rating must be high, medium or low")
        if ready not in {"high", "medium", "low", "unknown"}:
            out.append(f"{g}: readiness must be high, medium, low or unknown")
        if len((r.get("what_changes") or "").split()) < 4:
            out.append(f"{g}: say what actually changes for them day to day")
        if not (r.get("communication") or "").strip():
            out.append(f"{g}: no communication planned")
        if not (r.get("owner") or "").strip():
            out.append(f"{g}: nobody owns the change for this group")
        if rating == "high":
            if not (r.get("training") or "").strip():
                out.append(f"{g}: high impact with no training")
            if not (r.get("support") or "").strip():
                out.append(f"{g}: high impact with no support after go-live")
            if ready == "unknown":
                out.append(f"{g}: high impact and readiness unknown: ask a few of them before go-live")
            if ready == "low":
                out.append(f"{g}: high impact and low readiness: do not go live until this changes")
    if rows and not any((r.get("rating") or "").strip().lower() == "high" for r in rows):
        out.append("no group is rated high: check you have not missed whose job really changes")
    return out


def attention_first(rows):
    ok = [r for r in rows if (r.get("rating") or "").strip().lower() in LEVEL]
    ready = {"low": 3, "unknown": 3, "medium": 2, "high": 1}
    ok.sort(key=lambda r: (-LEVEL[r["rating"].strip().lower()], -ready.get((r.get("readiness") or "").strip().lower(), 3)))
    return ok


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as f:
        rows = list(csv.DictReader(f))
    found = check(rows)
    print("\n".join(found) if found else "Change impact table OK.")
    print("Attention first:")
    for r in attention_first(rows)[:3]:
        print(f"  {r['group']} (impact {r['rating']}, readiness {r['readiness']})")
    sys.exit(1 if found else 0)

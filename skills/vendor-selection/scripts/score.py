#!/usr/bin/env python3
"""Weighted scorecard for comparing vendors or options.

Input JSON:
{"criteria": {"Cost": 30, "Fit": 40, "Support": 30},
 "scores": {"Vendor A": {"Cost": 4, "Fit": 3, "Support": 5}, ...}}
Weights must add up to 100. Scores are 1-5.
Optional "knockouts": {"Vendor A": ["no EU data residency"]} disqualifies a vendor
before scoring, as a must-have it fails.
"""
import json
import sys


def excluded(data):
    """Vendors with at least one failed must-have: they are not scored."""
    return {v: why for v, why in data.get("knockouts", {}).items() if why}


def score(data):
    weights = data["criteria"]
    if round(sum(weights.values()), 6) != 100:
        raise ValueError(f"weights add up to {sum(weights.values())}, not 100")
    out = {}
    out_of_race = excluded(data)
    for vendor, s in data["scores"].items():
        if vendor in out_of_race:
            continue
        missing = set(weights) - set(s)
        if missing:
            raise ValueError(f"{vendor} has no score for {sorted(missing)}")
        for k, v in s.items():
            if k in weights and not 1 <= v <= 5:
                raise ValueError(f"{vendor}/{k}: score {v} is outside 1-5")
        out[vendor] = round(sum(weights[k] * s[k] for k in weights) / 100, 2)
    if not out:
        raise ValueError("every vendor fails a must-have: relax the must-have or widen the search")
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def robustness(data, shift=10):
    """Move `shift` weight points onto, then off, each criterion (others scale to
    keep the total at 100). Returns the changes that make a different vendor win."""
    base = next(iter(score(data)))
    flips = []
    w = data["criteria"]
    for k in w:
        for delta in (shift, -shift):
            nk = min(100, max(0, w[k] + delta))
            if nk == w[k] or w[k] == 100:
                continue
            scale = (100 - nk) / (100 - w[k])
            new = {j: (nk if j == k else w[j] * scale) for j in w}
            winner = next(iter(score({"criteria": new, "scores": data["scores"]})))
            if winner != base:
                flips.append(f"{'+' if delta > 0 else ''}{delta} on {k}: {winner} wins instead of {base}")
    return flips


def margin(data):
    ranked = list(score(data).items())
    return round(ranked[0][1] - ranked[1][1], 2) if len(ranked) > 1 else None


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    d = json.load(src)
    for v, why in excluded(d).items():
        print(f"Excluded: {v} (fails: {'; '.join(why)})")
    for v, sc in score(d).items():
        print(f"{sc:.2f}  {v}")
    flips = robustness(d)
    print(f"Lead over second place: {margin(d)}")
    print("Winner holds under every 10-point weight shift." if not flips else "Close call, the winner changes if:")
    for f in flips:
        print("  " + f)

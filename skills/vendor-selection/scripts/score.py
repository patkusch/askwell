#!/usr/bin/env python3
"""Weighted scorecard for comparing vendors or options.

Input JSON:
{"criteria": {"Cost": 30, "Fit": 40, "Support": 30},
 "scores": {"Vendor A": {"Cost": 4, "Fit": 3, "Support": 5}, ...}}
Weights must add up to 100. Scores are 1-5.
"""
import json
import sys


def score(data):
    weights = data["criteria"]
    if round(sum(weights.values()), 6) != 100:
        raise ValueError(f"weights add up to {sum(weights.values())}, not 100")
    out = {}
    for vendor, s in data["scores"].items():
        missing = set(weights) - set(s)
        if missing:
            raise ValueError(f"{vendor} has no score for {sorted(missing)}")
        for k, v in s.items():
            if k in weights and not 1 <= v <= 5:
                raise ValueError(f"{vendor}/{k}: score {v} is outside 1-5")
        out[vendor] = round(sum(weights[k] * s[k] for k in weights) / 100, 2)
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    for v, s in score(json.load(src)).items():
        print(f"{s:.2f}  {v}")

#!/usr/bin/env python3
"""Rank backlog items by RICE or WSJF.

CSV columns
  rice: id,name,reach,impact,confidence,effort      (confidence 0-1)
  wsjf: id,name,business_value,time_criticality,risk_reduction,job_size
Usage: score.py rice|wsjf items.csv
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


if __name__ == "__main__":
    method, path = sys.argv[1], sys.argv[2]
    with open(path, newline="") as f:
        for i, r in enumerate(rank(method, list(csv.DictReader(f))), 1):
            print(f"{i}. {r['id']}  {r['name']}  score={r['score']}")

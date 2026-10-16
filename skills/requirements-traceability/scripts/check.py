#!/usr/bin/env python3
"""Find gaps in a requirements traceability matrix.

CSV columns: req_id,requirement,design_ref,test_ref,status
Reports requirements with no design, no test, or that are marked done
without a test. Blank cell = missing.
"""
import csv
import sys


def check(rows):
    problems = []
    seen = set()
    for r in rows:
        rid = (r.get("req_id") or "").strip()
        if not rid:
            problems.append("a row has no req_id")
            continue
        if rid in seen:
            problems.append(f"{rid}: listed twice")
        seen.add(rid)
        if not (r.get("design_ref") or "").strip():
            problems.append(f"{rid}: no design reference")
        if not (r.get("test_ref") or "").strip():
            problems.append(f"{rid}: no test")
            if (r.get("status") or "").strip().lower() in {"done", "delivered", "live"}:
                problems.append(f"{rid}: marked {r['status']} but nothing tests it")
    return problems


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as f:
        found = check(list(csv.DictReader(f)))
    print("\n".join(found) if found else "No gaps found.")
    sys.exit(1 if found else 0)

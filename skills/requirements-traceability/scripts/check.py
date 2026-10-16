#!/usr/bin/env python3
"""Find gaps in a requirements traceability matrix.

CSV columns: req_id,requirement,design_ref,test_ref,status
Reports requirements with no design, no test, or that are marked done
without a test. Blank cell = missing. Several tests in one cell: separate with ;
Optional: --tests tests.csv (column test_id) also finds tests that no
requirement uses, and test_refs that name a test that does not exist.
"""
import csv
import sys


def check(rows, tests=None):
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
    if tests is not None:
        known = {t.strip() for t in tests}
        used = set()
        for r in rows:
            for t in (r.get("test_ref") or "").split(";"):
                t = t.strip()
                if not t:
                    continue
                used.add(t)
                if t not in known:
                    problems.append(f"{(r.get('req_id') or '?').strip()}: test {t} does not exist")
        for t in sorted(known - used):
            problems.append(f"{t}: tests nothing (no requirement points at it)")
    return problems


if __name__ == "__main__":
    args = sys.argv[1:]
    tests = None
    if "--tests" in args:
        i = args.index("--tests")
        with open(args[i + 1], newline="") as tf:
            tests = [r["test_id"] for r in csv.DictReader(tf)]
        del args[i:i + 2]
    with open(args[0], newline="") as f:
        found = check(list(csv.DictReader(f)), tests)
    print("\n".join(found) if found else "No gaps found.")
    sys.exit(1 if found else 0)

#!/usr/bin/env python3
"""Check a RAID log and rank what needs attention.

CSV columns: id,type,description,likelihood,impact,owner,due,status,last_reviewed
Dates are YYYY-MM-DD. likelihood and impact are 1-5 (risks only).
Usage: raid.py log.csv [--today YYYY-MM-DD]
"""
import csv
import sys
from datetime import date, datetime

CLOSED = {"closed", "done", "resolved", "accepted"}


def d(s):
    s = (s or "").strip()
    return datetime.strptime(s, "%Y-%m-%d").date() if s else None


def review(rows, today):
    flags, ranked = [], []
    for r in rows:
        if (r.get("status") or "").strip().lower() in CLOSED:
            continue
        i = r["id"]
        if not (r.get("owner") or "").strip():
            flags.append(f"{i}: no owner")
        due = d(r.get("due"))
        if due and due < today:
            flags.append(f"{i}: overdue by {(today - due).days} days")
        if not due:
            flags.append(f"{i}: no due date")
        seen = d(r.get("last_reviewed"))
        if seen is None or (today - seen).days > 30:
            flags.append(f"{i}: not reviewed in over 30 days")
        if (r.get("type") or "").strip().lower() == "risk":
            try:
                s = int(r["likelihood"]) * int(r["impact"])
            except (ValueError, KeyError):
                flags.append(f"{i}: risk without likelihood and impact (1-5)")
                continue
            ranked.append((s, i, r["description"]))
            if s >= 15:
                flags.append(f"{i}: score {s}, take to the sponsor")
    ranked.sort(reverse=True)
    return flags, ranked


if __name__ == "__main__":
    today = date.today()
    if "--today" in sys.argv:
        today = d(sys.argv[sys.argv.index("--today") + 1])
    with open(sys.argv[1], newline="") as f:
        flags, ranked = review(list(csv.DictReader(f)), today)
    print("Top risks:")
    for s, i, desc in ranked[:5]:
        print(f"  {s:>2}  {i}  {desc}")
    print("Needs attention:" if flags else "Nothing needs attention.")
    for fl in flags:
        print("  " + fl)
    sys.exit(1 if flags else 0)

#!/usr/bin/env python3
"""Check a RAID log and rank what needs attention.

CSV columns: id,type,description,likelihood,impact,owner,due,status,last_reviewed
Dates are YYYY-MM-DD. likelihood and impact are 1-5 (risks only).
Usage: raid.py log.csv [--today YYYY-MM-DD] [--grid]
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


def grid(rows):
    """Text heat map: impact across, likelihood down (5 at the top). Open, rated risks only."""
    cells = {}
    for r in rows:
        if (r.get("type") or "").strip().lower() != "risk" or (r.get("status") or "").strip().lower() in CLOSED:
            continue
        try:
            l, i = int(r["likelihood"]), int(r["impact"])
        except (ValueError, KeyError, TypeError):
            continue
        if 1 <= l <= 5 and 1 <= i <= 5:
            cells.setdefault((l, i), []).append(r["id"])
    width = max([len(",".join(v)) for v in cells.values()] + [8]) + 2
    lines = ["Likelihood".ljust(11) + "".join(f"impact {i}".center(width) for i in range(1, 6))]
    for l in range(5, 0, -1):
        row = "".join((",".join(cells.get((l, i), [])) or ("*" if l * i >= 15 else ".")).center(width) for i in range(1, 6))
        lines.append(f"{l}".ljust(11) + row)
    lines.append("* = a high-score square (15 or more) with nothing in it; . = empty")
    return "\n".join(lines)


if __name__ == "__main__":
    today = date.today()
    if "--today" in sys.argv:
        today = d(sys.argv[sys.argv.index("--today") + 1])
    with open(sys.argv[1], newline="") as f:
        all_rows = list(csv.DictReader(f))
    flags, ranked = review(all_rows, today)
    if "--grid" in sys.argv:
        print(grid(all_rows))
    print("Top risks:")
    for s, i, desc in ranked[:5]:
        print(f"  {s:>2}  {i}  {desc}")
    print("Needs attention:" if flags else "Nothing needs attention.")
    for fl in flags:
        print("  " + fl)
    sys.exit(1 if flags else 0)

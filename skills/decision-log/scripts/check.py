#!/usr/bin/env python3
"""Check a decision log.

CSV columns: id,date,decision,options,reason,decided_by,status,superseded_by,review_by
status: proposed | decided | superseded.  options separated by ;  dates YYYY-MM-DD.
Usage: check.py log.csv [--today YYYY-MM-DD]
"""
import csv
import sys
from datetime import date, datetime


def day(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return "bad"


def check(rows, today):
    out, by_id = [], {}
    for r in rows:
        i = (r.get("id") or "").strip()
        if not i:
            out.append("a row has no id")
            continue
        if i in by_id:
            out.append(f"{i}: id used twice")
        by_id[i] = r
    for r in [r for r in rows if (r.get("id") or "").strip()]:
        i = r["id"].strip()
        d = day(r.get("date"))
        if d is None or d == "bad":
            out.append(f"{i}: date missing or not YYYY-MM-DD")
        status = (r.get("status") or "").strip().lower()
        if status not in {"proposed", "decided", "superseded"}:
            out.append(f"{i}: status must be proposed, decided or superseded")
        dec = (r.get("decision") or "").strip()
        if not dec:
            out.append(f"{i}: no decision written")
        elif dec.endswith("?"):
            out.append(f"{i}: the decision is a question; state what was decided")
        if len([o for o in (r.get("options") or "").split(";") if o.strip()]) < 2:
            out.append(f"{i}: fewer than two options recorded (what else was considered?)")
        if len((r.get("reason") or "").split()) < 6:
            out.append(f"{i}: reason is too short to explain the choice later")
        if status in {"decided", "superseded"} and not (r.get("decided_by") or "").strip():
            out.append(f"{i}: no one named as the decision maker")
        sup = (r.get("superseded_by") or "").strip()
        if status == "superseded":
            if not sup:
                out.append(f"{i}: superseded but does not say by which decision")
            elif sup not in by_id:
                out.append(f"{i}: superseded by {sup}, which is not in the log")
            else:
                nd = day(by_id[sup].get("date"))
                if isinstance(d, date) and isinstance(nd, date) and nd < d:
                    out.append(f"{i}: superseded by {sup}, which is dated earlier")
        elif sup:
            out.append(f"{i}: names {sup} as its replacement but its status is {status or 'blank'}")
        if status == "proposed" and isinstance(d, date) and (today - d).days > 14:
            out.append(f"{i}: proposed {(today - d).days} days ago and still undecided")
        rb = day(r.get("review_by"))
        if rb == "bad":
            out.append(f"{i}: review_by is not YYYY-MM-DD")
        elif isinstance(rb, date) and rb < today and status == "decided":
            out.append(f"{i}: review date {rb} has passed")
    return out


if __name__ == "__main__":
    today = date.today()
    if "--today" in sys.argv:
        today = day(sys.argv[sys.argv.index("--today") + 1])
    with open(sys.argv[1], newline="") as f:
        found = check(list(csv.DictReader(f)), today)
    print("\n".join(found) if found else "Decision log OK.")
    sys.exit(1 if found else 0)

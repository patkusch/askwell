#!/usr/bin/env python3
"""Check a meeting agenda held as JSON.

{"purpose": "Decide the refund approval limit", "date": "2026-11-05", "minutes": 45,
 "attendees": 6, "pre_reads_sent": "2026-11-02",
 "items": [{"topic": "Actions from last meeting", "owner": "Chair", "minutes": 5, "outcome": "inform"},
           {"topic": "Refund limit", "owner": "Priya", "minutes": 20, "outcome": "decide"}]}
outcome is one of: decide, discuss, inform.
"""
import json
import re
import sys
from datetime import datetime


def day(s):
    try:
        return datetime.strptime(str(s), "%Y-%m-%d").date()
    except ValueError:
        return None


def check(a):
    out = []
    purpose = str(a.get("purpose", "")).strip()
    if not purpose:
        out.append("no purpose: say what must be decided or produced")
    elif not re.search(r"\b(decide|agree|approve|choose|plan|review|produce|list|rank|sign|confirm|prioriti)", purpose, re.I):
        out.append("the purpose does not name an outcome (decide, agree, approve, plan...)")
    total = a.get("minutes")
    items = a.get("items", [])
    if not isinstance(total, int) or total <= 0:
        out.append("meeting length in minutes is missing")
        total = None
    if not items:
        out.append("no agenda items")
        return out
    used = sum(int(i.get("minutes", 0)) for i in items)
    if total and used > total:
        out.append(f"items add up to {used} minutes but the meeting is {total}")
    elif total and used < 0.8 * total:
        out.append(f"items fill {used} of {total} minutes: shorten the meeting")
    if len(items) > 7:
        out.append(f"{len(items)} items: nobody holds more than seven in their head")
    kinds = [str(i.get("outcome", "")).lower() for i in items]
    for i in items:
        t = i.get("topic", "(no topic)")
        if not str(i.get("owner", "")).strip():
            out.append(f"'{t}': no owner to lead it")
        if str(i.get("outcome", "")).lower() not in {"decide", "discuss", "inform"}:
            out.append(f"'{t}': outcome must be decide, discuss or inform")
    decide_time = sum(int(i.get("minutes", 0)) for i in items if str(i.get("outcome", "")).lower() == "decide")
    if "decide" in kinds and decide_time < 10:
        out.append(f"only {decide_time} minutes set aside to decide: it was probably decided before the meeting, or will not be decided")
    if all(k == "inform" for k in kinds):
        out.append("every item is 'inform': send it as an email instead")
    inform_time = sum(int(i.get("minutes", 0)) for i in items if str(i.get("outcome", "")).lower() == "inform")
    if used and inform_time / used > 0.3:
        out.append(f"{inform_time} of {used} minutes are one-way information: send it as a pre-read")
    if not re.search(r"action", str(items[0].get("topic", "")), re.I):
        out.append("the first item should review the actions from last time")
    if isinstance(a.get("attendees"), int) and "decide" in kinds and a["attendees"] > 8:
        out.append(f"{a['attendees']} attendees for a decision: invite those who decide and those who know")
    d, sent = day(a.get("date")), day(a.get("pre_reads_sent"))
    if d is None:
        out.append("date must be YYYY-MM-DD")
    if not a.get("pre_reads_sent"):
        out.append("no pre-read sent date: send papers two days ahead")
    elif sent is None:
        out.append("pre_reads_sent must be YYYY-MM-DD")
    elif d and (d - sent).days < 2:
        out.append("pre-reads went out less than two days ahead: people will not have read them")
    return out


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    found = check(json.load(src))
    print("\n".join(found) if found else "Agenda OK.")
    sys.exit(1 if found else 0)

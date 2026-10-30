#!/usr/bin/env python3
"""Check a workshop plan held as JSON.

{"output": "A ranked list of the top five pain points, each with an owner",
 "start": "09:30", "end": "12:00", "attendees": 8, "parking_lot": true,
 "blocks": [{"minutes": 10, "topic": "Opening", "owner": "Facilitator",
             "outcome": "Output, agenda and ground rules agreed", "method": "Talk"}]}
A block with "break" in its topic needs no owner or outcome.
"""
import json
import re
import sys


def mins(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def check(p):
    out = []
    output = str(p.get("output", "")).strip()
    if not output:
        out.append("no stated output: if you cannot say what the workshop will produce, do not hold it")
    elif not re.search(r"\b(list|decision|decide|ranked|ranking|map|agreed|plan|set of|options?|owner|priorit)", output, re.I):
        out.append("the output is not something you can hold in your hand (a list, a decision, a map...)")
    try:
        total_time = mins(p["end"]) - mins(p["start"])
    except (KeyError, ValueError, AttributeError):
        total_time = None
        out.append("start and end must be HH:MM")
    n = p.get("attendees")
    if not isinstance(n, int):
        out.append("number of attendees is missing")
    elif n < 4:
        out.append(f"{n} attendees: a meeting would do")
    elif n > 12:
        out.append(f"{n} attendees: split into two groups or cut to those who must agree")
    blocks = p.get("blocks", [])
    if not blocks:
        out.append("no agenda blocks")
        return out
    used = sum(int(b.get("minutes", 0)) for b in blocks)
    if total_time is not None:
        if used > total_time:
            out.append(f"agenda adds up to {used} minutes but only {total_time} are available")
        elif used < 0.9 * total_time:
            out.append(f"agenda fills {used} of {total_time} minutes: add slack or shorten the slot")
    first, last = blocks[0], blocks[-1]
    if not re.search(r"open|welcome|intro|kick", str(first.get("topic", "")), re.I):
        out.append("no opening block to agree the output, agenda and ground rules")
    if not re.search(r"clos|wrap|next steps|actions", str(last.get("topic", "")), re.I):
        out.append("no closing block to agree actions with owners and dates")
    run = 0
    for b in blocks:
        t = str(b.get("topic", ""))
        m = int(b.get("minutes", 0))
        if re.search(r"break|lunch|coffee", t, re.I):
            run = 0
            continue
        run += m
        for field in ("owner", "outcome", "method"):
            if not str(b.get(field, "")).strip():
                out.append(f"'{t}': no {field}")
        if m > 60:
            out.append(f"'{t}': {m} minutes in one block: split it or change the method halfway")
        if run > 90:
            out.append(f"more than 90 minutes without a break by the end of '{t}'")
            run = 0
    methods = " ".join(str(b.get("method", "")) for b in blocks).lower()
    if not re.search(r"silent|write|sticky|individually|own", methods):
        out.append("no silent writing step: without it the senior voice sets the answer")
    if not p.get("parking_lot"):
        out.append("no parking lot: off-topic points will derail a block")
    return out


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    found = check(json.load(src))
    print("\n".join(found) if found else "Workshop plan OK.")
    sys.exit(1 if found else 0)

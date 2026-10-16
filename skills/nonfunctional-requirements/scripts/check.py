#!/usr/bin/env python3
"""Check non-functional requirements.

CSV columns: id,area,requirement,how_tested,priority
Reports requirements with no measurable number, no test, a bad priority,
performance limits with no load stated, and checklist areas nobody has covered.
"""
import csv
import re
import sys

AREAS = ["performance", "availability", "capacity", "security", "privacy", "audit",
         "accessibility", "usability", "compatibility", "recovery", "support", "legal"]
PRIORITIES = {"must", "should", "could", "wont"}
UNIT = re.compile(r"\d[\d,.]*\s*((business |working |calendar )?|)(%|ms|milliseconds?|seconds?|secs?|minutes?|mins?|hours?|days?|years?|months?|weeks?|users?|requests?|"
                  r"records?|mb|gb|tb|kb|per|/)|wcag\s*\d|\b\d{2,}\b", re.I)
# these areas can be met by naming a standard or a rule instead of a number
STANDARD_OK = {"accessibility", "security", "privacy", "legal", "compatibility", "audit", "support", "usability"}
LOAD = re.compile(r"\b(users?|requests?|records?|concurrent|load|transactions?|per (second|minute|hour|day)|simultaneous)\b", re.I)


def check(rows):
    out, covered = [], set()
    for r in rows:
        i = (r.get("id") or "?").strip()
        area = (r.get("area") or "").strip().lower()
        text = (r.get("requirement") or "").strip()
        covered.add(area)
        if area not in AREAS:
            out.append(f"{i}: area '{area}' is not one of the checklist areas")
        if not text:
            out.append(f"{i}: no requirement text")
            continue
        has_number = bool(UNIT.search(text))
        if not has_number and area not in STANDARD_OK:
            out.append(f"{i}: no measurable number or unit ({area})")
        elif not has_number and len(text.split()) < 5:
            out.append(f"{i}: too vague to test ('{text}'): say what is allowed, who, or which standard")
        if area == "performance" and has_number and not LOAD.search(text):
            out.append(f"{i}: a speed with no load stated (how many users or requests?)")
        if area == "availability" and not re.search(r"%|hours?|minutes?|\d{2}:\d{2}", text):
            out.append(f"{i}: availability with no percentage or hours")
        if not (r.get("how_tested") or "").strip():
            out.append(f"{i}: no way to test it")
        pr = (r.get("priority") or "").strip().lower().replace("'", "").replace("won't", "wont")
        if pr not in PRIORITIES:
            out.append(f"{i}: priority must be must/should/could/wont")
    missing = [a for a in AREAS if a not in covered]
    if missing:
        out.append("not covered yet: " + ", ".join(missing) + " (ask, or record that it does not apply)")
    return out


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as f:
        found = check(list(csv.DictReader(f)))
    print("\n".join(found) if found else "Non-functional requirements OK.")
    sys.exit(1 if found else 0)

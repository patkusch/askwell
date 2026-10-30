#!/usr/bin/env python3
"""Check an elicited requirements list.

CSV columns: id,need,type,source,who,date,status,priority
type: business|user|system|data   status: confirmed|assumed|disputed
who: a named person or a named group with a contact. Priority: must|should|could|wont
"""
import csv
import re
import sys
from datetime import datetime

TECH = ["database", "api", "button", "dropdown", "screen", "dashboard", "app", "portal", "excel", "spreadsheet", "chatbot", "microservice", "cloud"]
VAGUE_WHO = {"everyone", "everybody", "users", "all users", "stakeholders", "management", "the business", "staff", "people", "someone", "tbc", "unknown", ""}
TYPES = {"business", "user", "system", "data"}


def check(rows):
    out, seen = [], set()
    assumed = 0
    for r in rows:
        i = (r.get("id") or "").strip() or "?"
        if i in seen:
            out.append(f"{i}: id used twice")
        seen.add(i)
        need = (r.get("need") or "").strip()
        if not need:
            out.append(f"{i}: no need written")
        t = (r.get("type") or "").strip().lower()
        if t not in TYPES:
            out.append(f"{i}: type must be business, user, system or data")
        if t == "business":
            for w in TECH:
                if re.search(rf"\b{w}\b", need.lower()):
                    out.append(f"{i}: a business need that names a technology ('{w}'): ask what it is for")
                    break
        if re.search(r"\b(everyone|everybody|all users) (wants?|needs?)\b", need.lower()):
            out.append(f"{i}: 'everyone wants this': find one person who does")
        if not (r.get("source") or "").strip():
            out.append(f"{i}: no source (interview, document, observation)")
        if (r.get("who") or "").strip().lower() in VAGUE_WHO:
            out.append(f"{i}: 'who' is not a named person: you cannot go back and ask")
        d = (r.get("date") or "").strip()
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except ValueError:
            out.append(f"{i}: date missing or not YYYY-MM-DD")
        s = (r.get("status") or "").strip().lower()
        if s not in {"confirmed", "assumed", "disputed"}:
            out.append(f"{i}: status must be confirmed, assumed or disputed")
        assumed += s == "assumed"
        p = (r.get("priority") or "").strip().lower().replace("'", "").replace("won't", "wont")
        if p not in {"must", "should", "could", "wont"}:
            out.append(f"{i}: priority must be must, should, could or wont")
        if s == "assumed" and p == "must":
            out.append(f"{i}: a Must that is only assumed: confirm it with the source")
    if rows and assumed / len(rows) > 0.5:
        out.append(f"{assumed} of {len(rows)} requirements are only assumed: talk to more people before writing on")
    return out


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as f:
        found = check(list(csv.DictReader(f)))
    print("\n".join(found) if found else "Requirements list OK.")
    sys.exit(1 if found else 0)

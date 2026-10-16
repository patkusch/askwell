#!/usr/bin/env python3
"""Check a data dictionary CSV.

Columns: field,meaning,type,allowed_values,required,source,owner,rules,sensitivity,retention
sensitivity is one of: none, personal, sensitive, financial, confidential (or blank).
"""
import csv
import re
import sys

STOP = {"a", "an", "the", "of", "is", "are", "to", "for", "and", "or", "in", "who", "that", "which", "this"}
MONEY = re.compile(r"(amount|price|cost|fee|total|balance|salary|revenue|value)", re.I)
PERSONAL = {"personal", "sensitive", "financial"}


def words(s):
    return {w for w in re.findall(r"[a-z]+", s.lower().replace("_", " ")) if w not in STOP}


def check(rows):
    out, seen = [], {}
    for r in rows:
        f = (r.get("field") or "").strip()
        if not f:
            out.append("a row has no field name")
            continue
        key = f.lower()
        if key in seen:
            out.append(f"{f}: defined twice")
        seen[key] = True
        meaning = (r.get("meaning") or "").strip()
        if not meaning:
            out.append(f"{f}: no meaning")
        else:
            mw, fw = words(meaning), words(f)
            if len(meaning.split()) < 4:
                out.append(f"{f}: meaning is too short to be a definition")
            elif mw and mw <= fw | {"customer", "record", "value", "data"}:
                out.append(f"{f}: meaning only repeats the field name")
        for col in ("type", "source", "owner"):
            if not (r.get(col) or "").strip():
                out.append(f"{f}: no {col}")
        typ = (r.get("type") or "").lower()
        rules = (r.get("rules") or "").lower() + " " + typ
        if re.search(r"date ?time|timestamp", typ) and not re.search(r"utc|time ?zone|tz|local|gmt|offset", rules):
            out.append(f"{f}: date-time with no time zone")
        if MONEY.search(f) and re.search(r"decimal|number|numeric|float|int|money", typ) and not re.search(r"currency|gbp|usd|eur|£|\$|€", rules):
            out.append(f"{f}: an amount with no currency stated")
        sens = (r.get("sensitivity") or "").strip().lower()
        if sens in PERSONAL and not (r.get("retention") or "").strip():
            out.append(f"{f}: {sens} data with no retention period")
        if sens in PERSONAL and re.search(r"free ?text|text \(free|notes?\b", typ + " " + key):
            out.append(f"{f}: free text that may hold {sens} data: restrict or review it")
        if (r.get("allowed_values") or "").strip() == "" and re.search(r"status|type|category|code|state", key):
            out.append(f"{f}: looks like a list of values but none are given")
    return out


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as f:
        found = check(list(csv.DictReader(f)))
    print("\n".join(found) if found else "Data dictionary OK.")
    sys.exit(1 if found else 0)

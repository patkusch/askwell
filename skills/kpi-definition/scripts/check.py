#!/usr/bin/env python3
"""Check KPI definitions are complete and measurable.

Input: JSON list of objects with name, purpose, formula, source, owner,
frequency, baseline, target, guard (what stops it being gamed), action.
"""
import json
import re
import sys

REQUIRED = ["name", "purpose", "formula", "source", "owner", "frequency", "baseline", "target", "guard", "action"]


def check(kpis):
    out = []
    names = set()
    for k in kpis:
        n = k.get("name") or "(no name)"
        if n in names:
            out.append(f"{n}: defined twice")
        names.add(n)
        for field in REQUIRED:
            if not str(k.get(field, "")).strip():
                out.append(f"{n}: no {field}")
        if k.get("target") and not re.search(r"\d", str(k["target"])):
            out.append(f"{n}: target has no number")
        if k.get("baseline") and not re.search(r"\d", str(k["baseline"])):
            out.append(f"{n}: baseline has no number (measure it before the project starts)")
        f = str(k.get("formula", ""))
        if f and not re.search(r"(÷|/|divided by|per|ratio|average|sum|count|number of|total)", f, re.I):
            out.append(f"{n}: formula does not say what is counted or divided")
    if len(kpis) > 8:
        out.append(f"{len(kpis)} KPIs: if everything is a KPI, nothing is")
    return out


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    found = check(json.load(src))
    print("\n".join(found) if found else "All KPIs complete.")
    sys.exit(1 if found else 0)

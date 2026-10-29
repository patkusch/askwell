#!/usr/bin/env python3
"""Check an options paper held as JSON.

{"decision": "...", "deadline": "2026-12-01",
 "options": [{"name": "...", "description": "...", "cost_one_off": "40-60k",
              "cost_running": "5-8k a year", "benefit": "...", "risks": ["..."]}],
 "recommendation": {"option": "...", "reason": "...", "biggest_risk": "...", "mitigation": "..."},
 "unknowns": ["..."]}
Costs are ranges: "40-60k", "40 to 60k", or {"low": 40, "high": 60}.
"""
import json
import re
import sys

NOTHING = re.compile(r"do(ing)? nothing|status quo|no change|leave as is|keep as is", re.I)


def is_range(v):
    if isinstance(v, dict):
        return "low" in v and "high" in v
    return bool(re.search(r"\d\s*(-|–|to)\s*\d", str(v)))


def has_figure(v):
    return bool(re.search(r"\d", json.dumps(v)))


def check(p):
    out = []
    for k in ("decision", "deadline"):
        if not str(p.get(k, "")).strip():
            out.append(f"no {k}")
    opts = p.get("options", [])
    if len(opts) < 3:
        out.append(f"{len(opts)} option(s): give at least 3 real choices")
    if len(opts) > 5:
        out.append(f"{len(opts)} options: cut to the 5 that are genuinely different")
    names = [o.get("name", "") for o in opts]
    if len(set(n.lower() for n in names)) != len(names):
        out.append("two options have the same name")
    if not any(NOTHING.search(n) for n in names):
        out.append("no 'do nothing' option: it has a cost too, so show it")
    for o in opts:
        n = o.get("name", "(unnamed)")
        for field in ("cost_one_off", "cost_running"):
            v = o.get(field)
            if v in (None, "", {}):
                out.append(f"{n}: no {field}")
            elif not has_figure(v):
                out.append(f"{n}: {field} has no figure")
            elif not is_range(v) and not NOTHING.search(n):
                out.append(f"{n}: {field} is a single figure: give a range")
        if not o.get("risks"):
            out.append(f"{n}: no risks listed")
        if not str(o.get("benefit", "")).strip():
            out.append(f"{n}: no benefit stated")
        if NOTHING.search(n) and not has_figure(o.get("cost_running", "")):
            out.append(f"{n}: do nothing is not free; put a figure on what continues to go wrong")
    rec = p.get("recommendation") or {}
    if not rec:
        out.append("no recommendation")
    else:
        if rec.get("option") not in names:
            out.append(f"recommended option '{rec.get('option')}' is not one of the options")
        if len(str(rec.get("reason", "")).split()) < 8:
            out.append("recommendation reason is too short")
        for k in ("biggest_risk", "mitigation"):
            if not str(rec.get(k, "")).strip():
                out.append(f"recommendation has no {k.replace('_', ' ')}")
        others = [len(str(o.get("description", "")).split()) for o in opts if o.get("name") != rec.get("option")]
        mine = [len(str(o.get("description", "")).split()) for o in opts if o.get("name") == rec.get("option")]
        if others and mine and mine[0] > 2.5 * (sum(others) / len(others)) and mine[0] > 40:
            out.append("the recommended option is described in far more detail than the others: it reads as a sales pitch")
    if not p.get("unknowns"):
        out.append("no unknowns listed: say what you do not know and how to find out")
    return out


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    found = check(json.load(src))
    print("\n".join(found) if found else "Options paper OK.")
    sys.exit(1 if found else 0)

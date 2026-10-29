#!/usr/bin/env python3
"""Check a gap analysis and say what to close first.

CSV columns: area,current,target,gap,impact,effort,action,owner
area: people|process|technology|data|policy.  impact, effort: H|M|L
When current and target are plain numbers, gap must equal target - current.
"""
import csv
import re
import sys

AREAS = ["people", "process", "technology", "data", "policy"]
LEVEL = {"h": 3, "high": 3, "m": 2, "medium": 2, "l": 1, "low": 1}


def num(s):
    m = re.fullmatch(r"\s*-?\d+(\.\d+)?\s*(%|min|mins|minutes|hours|days)?\s*", str(s or ""))
    return float(re.match(r"-?\d+(\.\d+)?", m.group(0).strip()).group(0)) if m else None


def check(rows):
    out, covered = [], set()
    for n, r in enumerate(rows, 1):
        tag = f"row {n} ({(r.get('area') or '?').strip()})"
        area = (r.get("area") or "").strip().lower()
        covered.add(area)
        if area not in AREAS:
            out.append(f"{tag}: area must be one of {', '.join(AREAS)}")
        cur, tgt = (r.get("current") or "").strip(), (r.get("target") or "").strip()
        if not cur or not tgt:
            out.append(f"{tag}: needs both a current and a target")
        elif cur.lower() == tgt.lower():
            out.append(f"{tag}: current and target are the same, so there is no gap")
        elif not re.search(r"\d", cur) or not re.search(r"\d", tgt):
            out.append(f"{tag}: current or target has no number: how will you know the gap is closed?")
        a, b, g = num(cur), num(tgt), num(r.get("gap"))
        if a is not None and b is not None and g is not None and abs((b - a) - g) > 1e-6 and abs(abs(b - a) - abs(g)) > 1e-6:
            out.append(f"{tag}: gap {r['gap']} does not match target - current = {b - a:g}")
        for col in ("impact", "effort"):
            if (r.get(col) or "").strip().lower() not in LEVEL:
                out.append(f"{tag}: {col} must be H, M or L")
        for col in ("action", "owner"):
            if not (r.get(col) or "").strip():
                out.append(f"{tag}: no {col}")
    missing = [a for a in AREAS if a not in covered]
    if rows and missing:
        out.append("no gaps looked at for: " + ", ".join(missing) + " (look, or say it does not apply)")
    return out


def close_first(rows):
    """High impact, low effort first."""
    ok = [r for r in rows if (r.get("impact") or "").strip().lower() in LEVEL and (r.get("effort") or "").strip().lower() in LEVEL]
    ok.sort(key=lambda r: (-LEVEL[r["impact"].strip().lower()], LEVEL[r["effort"].strip().lower()]))
    return ok


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as f:
        rows = list(csv.DictReader(f))
    found = check(rows)
    if found:
        print("\n".join(found))
    else:
        print("Gap analysis OK.")
    print("Close first:")
    for r in close_first(rows)[:3]:
        print(f"  {r['area']}: {r['current']} -> {r['target']}  (impact {r['impact']}, effort {r['effort']})  {r['action']}")
    sys.exit(1 if found else 0)

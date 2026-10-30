#!/usr/bin/env python3
"""Check a current-state step table and summarise where the time goes.

CSV columns: step,role,system,kind,volume_per_week,touch_minutes,wait_minutes,error_rate_pct,evidence
kind: normal|exception   evidence: measured|observed|estimated
Wait is the time the work sits before this step starts. Rates are percentages 0-100.
"""
import csv
import sys


def num(x):
    try:
        return float(str(x).strip())
    except ValueError:
        return None


def check(rows):
    out = []
    kinds = set()
    est = 0
    for n, r in enumerate(rows, 1):
        step = (r.get("step") or "").strip() or f"row {n}"
        for col in ("role", "system"):
            if not (r.get(col) or "").strip():
                out.append(f"{step}: no {col}")
        k = (r.get("kind") or "").strip().lower()
        if k not in {"normal", "exception"}:
            out.append(f"{step}: kind must be normal or exception")
        kinds.add(k)
        for col in ("volume_per_week", "touch_minutes", "wait_minutes", "error_rate_pct"):
            v = num(r.get(col))
            if v is None:
                out.append(f"{step}: {col} is missing or not a number")
            elif v < 0:
                out.append(f"{step}: {col} is negative")
            elif col == "error_rate_pct" and v > 100:
                out.append(f"{step}: error rate over 100%")
        ev = (r.get("evidence") or "").strip().lower()
        if ev not in {"measured", "observed", "estimated"}:
            out.append(f"{step}: evidence must be measured, observed or estimated")
        est += ev == "estimated"
        t, w = num(r.get("touch_minutes")), num(r.get("wait_minutes"))
        if t is not None and w is not None and t > 0 and w > 20 * t and ev == "estimated":
            out.append(f"{step}: waits {w:g} minutes for {t:g} of work and the wait is only an estimate: measure it")
    if rows and "exception" not in kinds:
        out.append("no exception steps: you have mapped the happy path only, and exceptions often cost the most")
    if rows and est / len(rows) > 0.5:
        out.append(f"{est} of {len(rows)} rows are only estimates: observe real cases before comparing a future state")
    return out


def summary(rows):
    normal = [r for r in rows if (r.get("kind") or "").strip().lower() == "normal" and (num(r.get("touch_minutes")) or 0) >= 0 and (num(r.get("wait_minutes")) or 0) >= 0
              and num(r.get("touch_minutes")) is not None and num(r.get("wait_minutes")) is not None]
    if not normal:
        return []
    touch = sum(num(r["touch_minutes"]) for r in normal)
    wait = sum(num(r["wait_minutes"]) for r in normal)
    worst_wait = max(normal, key=lambda r: num(r["wait_minutes"]))
    lines = [
        f"End to end on the normal path: {touch:g} minutes of work, {wait:g} minutes of waiting ({touch / (touch + wait):.0%} of the time is work)."
        if touch + wait else "No time recorded.",
        f"Longest wait: before '{worst_wait['step']}' ({num(worst_wait['wait_minutes']):g} minutes).",
    ]
    errs = [r for r in rows if num(r.get("error_rate_pct")) and num(r.get("volume_per_week"))]
    if errs:
        worst = max(errs, key=lambda r: num(r["error_rate_pct"]) * num(r["volume_per_week"]))
        lines.append(f"Most errors per week: '{worst['step']}' ({num(worst['error_rate_pct']) * num(worst['volume_per_week']) / 100:.1f}).")
    return lines


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as f:
        rows = list(csv.DictReader(f))
    found = check(rows)
    print("\n".join(found) if found else "Current-state table OK.")
    for l in summary(rows):
        print(l)
    sys.exit(1 if found else 0)

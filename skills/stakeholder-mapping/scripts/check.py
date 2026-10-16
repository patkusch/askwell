#!/usr/bin/env python3
"""Check a stakeholder register.

CSV columns: name,role,cares_about,power,interest,stance,engagement,owner
power/interest: high|low (h|l ok). stance: supporter|neutral|resistant.
"""
import csv
import sys

GROUPS = {
    "sponsor": ["sponsor", "executive", "director sponsor", "budget"],
    "people who do the work": ["operator", "agent", "analyst", "staff", "team member", "clerk", "handler", "user"],
    "customers": ["customer", "client", "citizen", "patient", "member"],
    "technology": ["it ", "technology", "engineer", "architect", "developer", "ict"],
    "risk, legal or compliance": ["legal", "compliance", "risk", "privacy", "audit", "security"],
    "finance": ["finance", "financial", "procurement", "budget holder"],
}
NORM = {"h": "high", "high": "high", "l": "low", "low": "low"}


def check(rows):
    out, names, roles = [], set(), []
    for r in rows:
        n = (r.get("name") or "").strip()
        if not n:
            out.append("a row has no name")
            continue
        if n.lower() in names:
            out.append(f"{n}: listed twice")
        names.add(n.lower())
        roles.append((r.get("role") or "").lower() + " ")
        power = NORM.get((r.get("power") or "").strip().lower())
        interest = NORM.get((r.get("interest") or "").strip().lower())
        stance = (r.get("stance") or "").strip().lower()
        if not power:
            out.append(f"{n}: power must be high or low")
        if not interest:
            out.append(f"{n}: interest must be high or low")
        if stance not in {"supporter", "neutral", "resistant"}:
            out.append(f"{n}: stance must be supporter, neutral or resistant")
        if not (r.get("engagement") or "").strip():
            out.append(f"{n}: no plan for how to engage")
        if not (r.get("owner") or "").strip():
            out.append(f"{n}: nobody on the team owns this relationship")
        cares = (r.get("cares_about") or "").strip()
        if stance == "resistant" and len(cares.split()) < 4:
            out.append(f"{n}: resistant but the reason is not written down (what do they stand to lose?)")
        if power == "high" and stance == "resistant" and "close" not in (r.get("engagement") or "").lower():
            out.append(f"{n}: high power and resistant: your biggest stakeholder risk: manage closely, not by newsletter")
        if power == "high" and interest == "high" and "close" not in (r.get("engagement") or "").lower() \
                and (r.get("engagement") or "").strip():
            out.append(f"{n}: high power and high interest should be managed closely (regular one-to-ones)")
    joined = " ".join(roles)
    missing = [g for g, kws in GROUPS.items() if not any(k in joined for k in kws)]
    if rows and missing:
        out.append("no one listed for: " + "; ".join(missing))
    return out


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as f:
        found = check(list(csv.DictReader(f)))
    print("\n".join(found) if found else "Stakeholder register OK.")
    sys.exit(1 if found else 0)

#!/usr/bin/env python3
"""Check a scope statement written with these headings:
Objective / In scope / Out of scope / Assumptions / Constraints / Change control.
Items under a heading start with "- ".
"""
import re
import sys

HEADINGS = ["objective", "in scope", "out of scope", "assumptions", "constraints", "change control"]
ACTIVITY = ["investigate", "support", "manage", "work on", "look at", "explore", "consider", "assist", "help with", "review options"]
VAGUE = ["etc", "various", "as needed", "as required", "and so on", "any other", "everything", "all aspects", "tbd"]
STOP = {"the", "a", "an", "of", "and", "to", "for", "in", "on", "all", "new"}


def parse(text):
    sec, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Za-z ]+?):\s*(.*)$", line)
        if m and m.group(1).strip().lower() in HEADINGS:
            cur = m.group(1).strip().lower()
            sec[cur] = [m.group(2).strip()] if m.group(2).strip() else []
        elif cur and line.strip():
            sec[cur].append(line.strip().lstrip("-• ").strip())
    return sec


def toks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP}


def check(text):
    s = parse(text)
    out = []
    for h in HEADINGS:
        if h not in s:
            out.append(f"missing '{h.title()}'")
        elif not s[h]:
            out.append(f"'{h.title()}' is empty")
    for item in s.get("in scope", []):
        low = item.lower()
        for a in ACTIVITY:
            if low.startswith(a):
                out.append(f"In scope '{item}': an activity, not a deliverable. Say what will exist when it is done")
                break
    for h in ("in scope", "out of scope"):
        for item in s.get(h, []):
            for v in VAGUE:
                if re.search(rf"\b{re.escape(v)}\b", item.lower()):
                    out.append(f"{h.title()} '{item}': vague ('{v}'); list the cases")
                    break
    if "out of scope" in s and 0 < len(s["out of scope"]) < 2:
        out.append("Out of scope has one item: name everything a reasonable person might assume is included")
    for a in s.get("in scope", []):
        for b in s.get("out of scope", []):
            ta, tb = toks(a), toks(b)
            if ta and tb and len(ta & tb) / len(ta | tb) >= 0.7:
                out.append(f"'{a}' is in scope and '{b}' is out of scope: they contradict")
    for item in s.get("in scope", []) + s.get("out of scope", []):
        if re.search(r"\b(phase 2|later|future|next phase)\b", item.lower()) and not re.search(r"\d{4}|q[1-4]|owner|by ", item.lower()):
            out.append(f"'{item}': deferred with no date or owner")
    cc = " ".join(s.get("change control", [])).lower()
    if cc and not re.search(r"\b(approv|decid|sign)", cc):
        out.append("Change control does not say who approves a change")
    if cc and not re.search(r"\b(cost|time|risk|impact|effort)\b", cc):
        out.append("Change control does not say what is assessed (cost, time, risk)")
    return out


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    found = check(text)
    print("\n".join(found) if found else "Scope statement OK.")
    sys.exit(1 if found else 0)

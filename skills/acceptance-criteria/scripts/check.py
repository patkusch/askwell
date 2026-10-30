#!/usr/bin/env python3
"""Check Given/When/Then scenarios.

Scenarios are separated by blank lines. Each should read:
Given ... / When ... / Then ...   (each on its own line or all on one)
Reports scenarios missing a part, parts out of order, vague results, and
sets of scenarios that never test a failure.
"""
import re
import sys

VAGUE = ["quickly", "fast", "easily", "user-friendly", "properly", "correctly", "appropriate", "as expected"]
FAILURE = ["error", "invalid", "cannot", "can't", "not allowed", "rejected", "denied", "expired",
           "fails", "failed", "missing", "blocked", "refused", "unavailable", "unchanged"]


def split_scenarios(text):
    return [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]


def check_scenario(block):
    low = block.lower()
    probs = []
    pos = {}
    for kw in ("given", "when", "then"):
        m = re.search(rf"\b{kw}\b", low)
        if not m:
            probs.append(f"missing '{kw.capitalize()}'")
        else:
            pos[kw] = m.start()
    if len(pos) == 3 and not (pos["given"] < pos["when"] < pos["then"]):
        probs.append("Given/When/Then are out of order")
    if len(re.findall(r"\bwhen\b", low)) > 1:
        probs.append("more than one 'When': probably two scenarios")
    for w in VAGUE:
        if re.search(rf"\b{re.escape(w)}\b", low):
            probs.append(f"vague word '{w}' in the result: say what can be seen or measured")
    if "then" in pos and len(re.findall(r"\band\b", low[pos["then"]:])) >= 3:
        probs.append("a long chain of results: split it so each can fail on its own")
    return probs


def check(text):
    blocks = split_scenarios(text)
    report = []
    for i, b in enumerate(blocks, 1):
        for p in check_scenario(b):
            report.append((i, p))
    set_level = []
    seen = {}
    for i, b in enumerate(blocks, 1):
        key = re.sub(r"\s+", " ", b.lower()).strip(" .")
        if key in seen:
            set_level.append(f"scenario {i} repeats scenario {seen[key]}: delete it or change the data so it tests something new")
        seen.setdefault(key, i)
    if blocks and not any(re.search(rf"\b{re.escape(f)}\b", b.lower()) for b in blocks for f in FAILURE):
        set_level.append("no scenario tests a failure (bad input, expired, denied, unavailable)")
    if 0 < len(blocks) < 3:
        set_level.append(f"only {len(blocks)} scenario(s): most stories need a normal case, a boundary and a failure")
    return report, set_level


if __name__ == "__main__":
    src = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    per, whole = check(src)
    for i, p in per:
        print(f"scenario {i}: {p}")
    for p in whole:
        print(f"set: {p}")
    print("Clean." if not per and not whole else f"{len(per) + len(whole)} problem(s).")
    sys.exit(1 if per or whole else 0)

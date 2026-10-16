#!/usr/bin/env python3
"""Check a use case written in the template from SKILL.md.

Headings are lines like "Main flow:". Steps are numbered "1." and
alternatives/exceptions are numbered by the step they branch from: "3a." / "4e.".
"""
import re
import sys

REQUIRED = ["name", "actor", "goal", "trigger", "preconditions", "main flow",
            "alternative flows", "exceptions", "postconditions"]
SCREEN = ["click", "button", "page", "screen", "field", "dropdown", "tab", "menu", "scroll", "textbox"]


def sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Za-z][A-Za-z ]+?):\s*(.*)$", line)
        if m and m.group(1).strip().lower() in REQUIRED:
            cur = m.group(1).strip().lower()
            out[cur] = [m.group(2)] if m.group(2).strip() else []
        elif cur is not None and line.strip():
            out[cur].append(line.strip())
    return out


def steps(lines, branch=False):
    pat = r"^(\d+)([a-z])\.\s*(.*)$" if branch else r"^(\d+)\.\s*(.*)$"
    found = []
    for l in lines:
        m = re.match(pat, l)
        if m:
            found.append(m.groups())
    return found


def check(text):
    s = sections(text)
    out = []
    for h in REQUIRED:
        if h not in s:
            out.append(f"missing '{h.title()}'")
        elif not s[h]:
            out.append(f"'{h.title()}' is empty")
    if "name" in s and s["name"] and len(s["name"][0].split()) < 2:
        out.append("name should be a verb and an object, like 'Approve a refund'")
    main = steps(s.get("main flow", []))
    nums = [int(n) for n, _ in main]
    if "main flow" in s:
        if nums != list(range(1, len(nums) + 1)):
            out.append("main flow steps are not numbered 1, 2, 3 in order")
        if len(main) < 3:
            out.append(f"main flow has {len(main)} step(s): too thin to be a use case")
        if len(main) > 12:
            out.append(f"main flow has {len(main)} steps: probably two goals, split it")
        for n, t in main:
            for w in SCREEN:
                if re.search(rf"\b{w}\b", t.lower()):
                    out.append(f"step {n} describes the screen ('{w}'): say what the person does, not where")
                    break
        for n, t in main:
            if re.search(r"\b(if|otherwise|else|unless)\b", t.lower()):
                out.append(f"step {n} contains a branch: move it to Alternative flows")
    for heading in ("alternative flows", "exceptions"):
        for n, letter, t in steps(s.get(heading, []), branch=True):
            if int(n) not in nums:
                out.append(f"{heading.title()}: {n}{letter} branches from step {n}, which is not in the main flow")
    if "exceptions" in s and not steps(s["exceptions"], branch=True):
        out.append("Exceptions has no numbered entries (like '4e. If the system is down...')")
    return out


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    found = check(text)
    print("\n".join(found) if found else "Use case OK.")
    sys.exit(1 if found else 0)

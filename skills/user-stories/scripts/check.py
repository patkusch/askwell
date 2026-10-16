#!/usr/bin/env python3
"""Check user stories, one per line, in the form
As a <role>, I want <capability>, so that <benefit>.
"""
import re
import sys

PATTERN = re.compile(r"^\s*as (?:an?|the)\s+(?P<role>.+?),?\s+i want( to)?\s+(?P<want>.+?),?\s+so that\s+(?P<why>.+?)\.?\s*$", re.I)
GENERIC_ROLES = {"user", "users", "person", "people", "someone", "customer service"}
SOLUTION_WORDS = ["database", "table", "api", "endpoint", "button", "dropdown", "screen", "page", "field", "json", "script"]
BIG_WORDS = ["manage", "everything", "entire", "full ", "complete "]
STOP = {"a", "an", "the", "to", "i", "be", "can", "my", "of", "and", "in", "it", "is", "for", "that", "so"}


def words(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP}


def check(line):
    text = line.strip()
    if not text:
        return []
    m = PATTERN.match(text)
    if not m:
        return ["not in the form 'As a <role>, I want <capability>, so that <benefit>'"]
    role, want, why = m["role"].strip(), m["want"].strip(), m["why"].strip()
    out = []
    if role.lower() in GENERIC_ROLES:
        out.append(f"role '{role}' is too general: name who exactly")
    if role.lower() in {"system", "the system", "application"}:
        out.append("a system is not a person: name who benefits")
    w, y = words(want), words(why)
    if w and len(w & y) / len(w) >= 0.6:
        out.append("'so that' repeats the 'I want': say the benefit, not the action again")
    if len(why.split()) < 3:
        out.append("benefit is too short to be a reason")
    low = want.lower()
    for s in SOLUTION_WORDS:
        if re.search(rf"\b{s}\b", low):
            out.append(f"'{s}' describes a solution, not a need")
            break
    for b in BIG_WORDS:
        if b in low + " ":
            out.append(f"'{b.strip()}' suggests a story too big for one sprint: split it")
            break
    if re.search(r"\band\b", low):
        out.append("'and' in the want: probably two stories")
    return out


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    bad = 0
    for n, line in enumerate(src, 1):
        for p in check(line):
            bad += 1
            print(f"line {n}: {p}\n    {line.strip()}")
    print("Clean." if not bad else f"{bad} problem(s).")
    sys.exit(1 if bad else 0)

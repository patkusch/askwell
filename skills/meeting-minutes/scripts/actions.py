#!/usr/bin/env python3
"""Pull action items out of meeting notes and flag the ones that are unowned or undated.

An action is a line that starts with ACTION / TODO / AI: or contains cues such as
"will", "to do", "can you", "I'll", "needs to", "by <date>".
"""
import re
import sys

CUE = re.compile(r"^\s*(action|todo|to-do|ai)\s*[:\-]|\b(i'll|i will|will|should|needs? to|can you|could you|please|must)\b|(?-i:\b(?!Agreed|Decided|Back|Due)[A-Z][a-z]+ to [a-z]+)", re.I)
DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}(/\d{2,4})?|(mon|tues?|wednes|thurs?|fri|satur|sun)day|tomorrow|next week|end of (the )?(day|week|month)|eod|eow|"
                  r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* \d{1,2})\b", re.I)
OWNER = re.compile(r"(^\s*(action|todo|to-do|ai)\s*[:\-]\s*@?(?-i:[A-Z][a-z]+)\b)|@\w+|(?-i:\b(?!Someone|Somebody|Anyone|Everyone|We|They)[A-Z][a-z]+ (will|to|needs to|should|must)\b)|\b(I'll|I will)\b|(?-i:^\s*(?!Action|Todo)[A-Z][a-z]+:\s)", re.I)
DECISION = re.compile(r"\b(decided|agreed|we'll go with|let's go with|approved)\b", re.I)


def extract(text):
    actions, decisions = [], []
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        if DECISION.search(s):
            decisions.append((n, s))
        if CUE.search(s):
            missing = []
            if not OWNER.search(s):
                missing.append("owner")
            if not DATE.search(s):
                missing.append("date")
            actions.append((n, s, missing))
    return actions, decisions


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    actions, decisions = extract(text)
    print(f"Decisions ({len(decisions)}):")
    for n, s in decisions:
        print(f"  line {n}: {s}")
    print(f"Actions ({len(actions)}):")
    bad = 0
    for n, s, miss in actions:
        tag = "" if not miss else f"   <-- needs {' and '.join(miss)}"
        bad += bool(miss)
        print(f"  line {n}: {s}{tag}")
    sys.exit(1 if bad else 0)

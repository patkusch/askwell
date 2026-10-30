#!/usr/bin/env python3
"""Flag requirements that cannot be tested or are ambiguous.

Reads one requirement per line (file or stdin) and prints the problems.
"""
import re
import sys

VAGUE = ["fast", "quick", "quickly", "easy", "easily", "user-friendly", "intuitive",
         "flexible", "robust", "seamless", "efficient", "adequate", "appropriate",
         "as appropriate", "if possible", "as needed", "state-of-the-art", "modern"]
QUANTITY = ["some", "several", "many", "few", "most", "numerous", "multiple", "various", "a lot of", "a number of", "a couple of"]
OPEN_ENDED = ["etc", "and so on", "and/or", "including but not limited to", "such as"]


def lint(line):
    text = line.strip()
    if not text:
        return []
    low = text.lower()
    out = []
    if not re.search(r"\b(shall|must)\b", low):
        out.append("no 'shall' or 'must': is this a requirement or a wish?")
    if re.search(r"\bshould\b", low):
        out.append("'should' is ambiguous: say must or leave it out")
    for w in VAGUE:
        if re.search(rf"\b{re.escape(w)}\b", low):
            out.append(f"vague word '{w}': give a number or a test")
    for w in OPEN_ENDED:
        if re.search(rf"(?<![\w]){re.escape(w)}(?![\w])", low):
            out.append(f"open-ended '{w}': list every case or drop it")
    if len(re.findall(r"\band\b", low)) >= 2:
        out.append("several 'and's: probably more than one requirement")
    if not re.search(r"\d", text) and re.search(r"\b(within|at least|at most|no more than)\b", low):
        out.append("a limit is mentioned but there is no number")
    for q in QUANTITY:
        if re.search(rf"\b{re.escape(q)}\b", low):
            out.append(f"vague quantity '{q}': how many?")
            break
    if re.search(r"\b(tbd|tbc|to be (decided|confirmed|determined))\b", low):
        out.append("unfinished (TBD/TBC): find the answer or log it as an open question")
    if re.match(r"\s*(it|this|that|they|these)\s+(shall|must)\b", low):
        out.append("starts with a pronoun: name who or what must do this")
    if re.search(r"\b(shall|must) be \w+(ed|en)\b", low) and not re.search(r"\bby\b", low):
        out.append("passive voice with no actor: who does it?")
    if re.search(r"\bas (required|needed|necessary|appropriate)\b", low):
        out.append("'as required/needed': say when it is required")
    return out


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    bad = 0
    for n, line in enumerate(src, 1):
        for p in lint(line):
            bad += 1
            print(f"line {n}: {p}\n    {line.strip()}")
    print("Clean." if not bad else f"{bad} problem(s).")
    sys.exit(1 if bad else 0)

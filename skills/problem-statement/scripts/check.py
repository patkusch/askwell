#!/usr/bin/env python3
"""Check a problem statement.

Expected shape: who struggles to do what, because (cause); this results in
(measured impact); we will know it is fixed when (measurable outcome).
"""
import re
import sys

SOLUTION = ["system", "tool", "app", "application", "portal", "dashboard", "platform", "software", "website",
            "ai", "automation", "automate", "crm", "erp", "chatbot", "database", "spreadsheet", "workflow engine", "integration"]


def check(text):
    t = " ".join(text.split())
    low = t.lower()
    out = []
    if not t:
        return ["empty"]
    words = len(t.split())
    if words < 25:
        out.append(f"{words} words: too short to hold who, cause, impact and success measure")
    if words > 120:
        out.append(f"{words} words: a problem statement should fit in one paragraph (under 120 words)")
    found = [w for w in SOLUTION if re.search(rf"\b{re.escape(w)}\b", low)]
    if found:
        out.append(f"mentions a solution ({', '.join(found)}): describe the problem, not the answer")
    if re.search(r"\b(lack of|need for|no (?:system|tool|app)|missing (?:a|an))\b", low):
        out.append("'lack of' / 'need for' a thing is a solution in disguise: say what goes wrong without it")
    if not re.search(r"\d", t):
        out.append("no number anywhere: add how often, how many, how much it costs (or say the baseline is unknown)")
    if not re.search(r"\bbecause\b|\bdue to\b|\bas a result of\b|\bsince\b", low):
        out.append("no cause (because...)")
    if not re.search(r"\b(results? in|leads? to|causes?|costs?|means|delays?)\b", low):
        out.append("no impact (this results in...)")
    if not re.search(r"\b(know|measure|success|fixed when|resolved when|target|goal|reduce|below|under|within|at least)\b", low):
        out.append("no success measure (we will know it is fixed when...)")
    if not re.search(r"\b(struggle|spend|cannot|can't|unable|wait|lose|have to|waste|miss|redo|retype|re-type)\w*\b", low):
        out.append("no clear 'who struggles to do what'")
    return out


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    found = check(text)
    print("\n".join(found) if found else "Problem statement OK.")
    sys.exit(1 if found else 0)

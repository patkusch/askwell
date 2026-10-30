#!/usr/bin/env python3
"""Check the structure of a business requirements document written in Markdown.

Headings are "#"-style. Requirements are table rows or list items that begin with an
ID such as BR-001, R12 or NFR-3 and contain a priority (must/should/could/wont).
"""
import re
import sys

SECTIONS = {
    "summary": r"summary|overview",
    "problem": r"problem|background|context",
    "objectives": r"objective|goal|success measure",
    "scope": r"scope",
    "stakeholders": r"stakeholder",
    "requirements": r"requirement",
    "risks": r"risk|assumption|dependenc|constraint",
    "sign-off": r"sign.?off|approval",
    "version history": r"version|revision|change history",
}
ID = re.compile(r"\b((?:BR|FR|NFR|R|REQ)-?\d+)\b")
PRI = re.compile(r"\b(must|should|could|won'?t)\b", re.I)


def headings(md):
    return [(len(m.group(1)), m.group(2).strip(), m.start()) for m in re.finditer(r"^(#{1,4})\s+(.+)$", md, re.M)]


def section_text(md, hs, idx):
    start = md.index("\n", hs[idx][2]) if "\n" in md[hs[idx][2]:] else len(md)
    end = hs[idx + 1][2] if idx + 1 < len(hs) else len(md)
    return md[start:end]


def check(md):
    out = []
    hs = headings(md)
    names = [h[1].lower() for h in hs if h[0] >= 2] or [h[1].lower() for h in hs]
    for key, pat in SECTIONS.items():
        if not any(re.search(pat, n) for n in names):
            out.append(f"no '{key}' section")
    sections = [h for h in hs if h[0] >= 2] or hs
    if sections and not re.search(SECTIONS["summary"], sections[0][1].lower()):
        out.append("the summary should come first: the reader may stop there")
    for i, (level, name, _) in enumerate(hs):
        if level < 2:
            continue  # the title is not a section
        body = section_text(md, hs, i)
        low = name.lower()
        if re.search(SECTIONS["summary"], low):
            n = len(body.split())
            if n > 300:
                out.append(f"summary is {n} words: keep it to half a page (300 words)")
            if n < 30:
                out.append("summary is too short to say the problem, the outcome and the decision needed")
        if re.search(SECTIONS["objectives"], low) and not re.search(r"\d", body):
            out.append("objectives have no number: how will anyone know they were met?")
        if re.search(SECTIONS["scope"], low) and "out of scope" not in body.lower() and "out-of-scope" not in body.lower() \
                and not any("out" in n and "scope" in n for n in names):
            out.append("scope does not say what is out of scope")
        if re.search(SECTIONS["sign-off"], low):
            if not re.search(r"date", body, re.I) or not re.search(r"name|role", body, re.I):
                out.append("sign-off needs name, role and date columns")
    reqs = [l for l in md.splitlines() if ID.search(l) and PRI.search(l)]
    ids = [ID.search(l).group(1) for l in reqs]
    if any(re.search(SECTIONS["requirements"], n) for n in names) and not reqs:
        out.append("no numbered requirements with a priority (like BR-001 ... Must)")
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        out.append(f"requirement ID used twice: {', '.join(dup)}")
    for l in md.splitlines():
        m = ID.search(l)
        if m and re.search(r"\b(shall|must)\b", l, re.I) and re.search(r"\b(fast|easy|user-friendly|etc\.?|and/or)\b", l, re.I):
            out.append(f"{m.group(1)}: vague wording; run requirements-writing on it")
    left = re.findall(r"\[(?:name|date|tbd|insert|your)[^\]]*\]|\bTBD\b|\bTBC\b|lorem ipsum", md, re.I)
    if left:
        out.append(f"{len(left)} unfinished placeholder(s) such as '{left[0]}'")
    return out


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    found = check(text)
    print("\n".join(found) if found else "BRD structure OK.")
    sys.exit(1 if found else 0)

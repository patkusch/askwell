#!/usr/bin/env python3
"""Check interview write-up notes.

Sections (a line "Name:" then lines starting "- "):
  Interviewee, Date, Goal, Findings, Pain points, Workarounds, Candidate requirements,
  Open questions, Next interviews
Each finding starts with [heard], [seen] or [inferred].
"""
import re
import sys

REQUIRED = ["interviewee", "date", "goal", "findings", "pain points", "candidate requirements", "open questions", "next interviews"]
LEADING = re.compile(r"\b(wouldn't a|don't you think|surely|isn't it true|wouldn't it be better)\b", re.I)


def parse(text):
    sec, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Za-z ]+?):\s*(.*)$", line)
        if m and m.group(1).strip().lower() in REQUIRED + ["workarounds"]:
            cur = m.group(1).strip().lower()
            sec[cur] = [m.group(2).strip()] if m.group(2).strip() else []
        elif cur and line.strip():
            sec[cur].append(line.strip().lstrip("-• ").strip())
    return sec


def check(text):
    s = parse(text)
    out = []
    for h in REQUIRED:
        if h not in s:
            out.append(f"missing '{h.title()}'")
        elif not s[h]:
            out.append(f"'{h.title()}' is empty")
    if s.get("date") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s["date"][0]):
        out.append("Date is not YYYY-MM-DD")
    if s.get("goal") and len(s["goal"][0].split()) < 5:
        out.append("Goal is too short to tell whether the interview achieved it")
    f = s.get("findings", [])
    labels = {"heard": 0, "seen": 0, "inferred": 0}
    for item in f:
        m = re.match(r"^\[(heard|seen|inferred)\]\s*(.+)$", item, re.I)
        if not m:
            out.append(f"finding not labelled [heard], [seen] or [inferred]: '{item[:50]}'")
        else:
            labels[m.group(1).lower()] += 1
    if f and labels["inferred"] > labels["heard"] + labels["seen"]:
        out.append("more of your own reading than what was said or seen: go back and check")
    if f and labels["seen"] == 0:
        out.append("nothing [seen]: watch a real case, because people describe what they should do, not what they do")
    for item in s.get("pain points", []):
        if not re.search(r"\d", item) and len(item.split()) < 6:
            out.append(f"pain point '{item}' has no detail: how often, how long, how bad?")
    for item in s.get("candidate requirements", []):
        if re.search(r"\b(wants?|asked for|said (?:they )?need)\b.*\b(dashboard|app|tool|portal|system)\b", item, re.I):
            out.append(f"'{item[:50]}' is a solution: go back to the need behind it")
    for item in s.get("open questions", []):
        if not re.search(r"\b(ask|find out|check|confirm|who|by)\b", item, re.I):
            out.append(f"open question '{item[:50]}' says no one is finding out")
    if LEADING.search(text):
        out.append("leading question in the notes: ask what happens, not whether your idea would help")
    if not re.search(r"sent back|confirmed with|play(ed)? back", text, re.I):
        out.append("nothing says the findings were sent back to the interviewee to correct")
    return out


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    found = check(text)
    print("\n".join(found) if found else "Interview notes OK.")
    sys.exit(1 if found else 0)

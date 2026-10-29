#!/usr/bin/env python3
"""Check an executive summary or status update for a busy reader.

Does the opening say what is wanted? Is it short? Does it use plain words, define
its acronyms, and give numbers and the cost of each choice?
"""
import re
import sys

JARGON = ["leverage", "synergy", "synergies", "utilise", "utilize", "going forward", "circle back", "deep dive", "holistic",
          "paradigm", "bandwidth", "low-hanging fruit", "move the needle", "touch base", "stakeholder buy-in", "best-of-breed",
          "end-to-end solution", "value-add", "robust", "seamless", "streamline", "enable", "empower"]
ASK = re.compile(r"\b(we recommend|i recommend|please (approve|decide|confirm|agree|sign)|decision (needed|required)|"
                 r"need(s)? (you|your|a decision|approval)|approve|for your decision|you (are asked|need) to|"
                 r"we (need|ask) you|we are asking)\b", re.I)
KNOWN = {"UK", "US", "EU", "PM", "AM", "OK", "IT", "HR", "CEO", "CFO", "CTO", "VAT", "PDF", "FAQ", "ID"}


def sentences(t):
    return [s for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s]


def check(text):
    t = " ".join(text.split())
    out = []
    if not t:
        return ["empty"]
    words = t.split()
    if len(words) > 250:
        out.append(f"{len(words)} words: an executive summary should fit in 250")
    opening = " ".join(words[:60])
    if not ASK.search(opening):
        out.append("the first 60 words do not say what you want the reader to decide or do")
    if not re.search(r"\d", t):
        out.append("no numbers: give at least one figure and what it means")
    if not re.search(r"\b(risk|cost|costs|if we do nothing|downside|trade-?off)\b", t, re.I):
        out.append("no cost or risk of the choice: the reader will ask")
    if not re.search(r"\b(by|before|on|within|deadline)\s+(\d{1,2}\s+\w+|\w+\s+\d{1,2}|\d{4}-\d{2}-\d{2}|monday|tuesday|wednesday|thursday|friday|the end of \w+|end of \w+|next \w+)", t, re.I):
        out.append("no date for the decision or action")
    for j in JARGON:
        if re.search(rf"\b{re.escape(j)}\b", t, re.I):
            out.append(f"jargon '{j}': say it plainly")
    ss = sentences(t)
    if ss:
        avg = len(words) / len(ss)
        if avg > 25:
            out.append(f"sentences average {avg:.0f} words: one idea per sentence, aim for under 20")
        long_ones = [s for s in ss if len(s.split()) > 40]
        if long_ones:
            out.append(f"{len(long_ones)} sentence(s) over 40 words: split them")
    if len(re.findall(r"\b(might|perhaps|possibly|maybe|could potentially|it seems)\b", t, re.I)) >= 3:
        out.append("three or more hedges: say what you know and what you don't, separately")
    seen = set()
    for m in re.finditer(r"\b([A-Z]{2,6})\b", t):
        a = m.group(1)
        if a in seen or a in KNOWN:
            continue
        seen.add(a)
        before = t[max(0, m.start() - 1):m.start()]
        if before != "(" and not re.search(rf"\({re.escape(a)}\)", t):
            out.append(f"acronym {a} is never explained")
    return out


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    found = check(text)
    print("\n".join(found) if found else "Summary OK.")
    sys.exit(1 if found else 0)

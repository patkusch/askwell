#!/usr/bin/env python3
"""Check a five-whys write-up.

Lines:
  Problem: <with a number and a date>
  Why 1: <because ...>   (up to Why 7)
  Evidence: <how you know, one line per claim>
  Root cause: <something the organisation controls>
  Fix: <what removes the cause>
  Measure: <how we will know it worked>
"""
import re
import sys

BLAME = ["forgot", "careless", "carelessness", "human error", "lazy", "mistake by", "negligen", "incompetent",
         "didn't care", "did not care", "should have known", "failed to follow", "not paying attention"]
WEAK_FIX = ["remind", "retrain", "re-train", "be more careful", "pay more attention", "training reminder", "send an email to all", "tell staff", "warn staff"]
STOP = {"the", "a", "an", "of", "to", "and", "in", "on", "for", "is", "was", "were", "are", "it", "that", "because", "no", "not", "by", "with"}


def toks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP}


def parse(text):
    d = {"why": [], "evidence": []}
    for line in text.splitlines():
        m = re.match(r"^\s*(problem|root cause|fix|measure)\s*:\s*(.+)$", line, re.I)
        if m:
            d[m.group(1).lower()] = m.group(2).strip()
            continue
        m = re.match(r"^\s*why\s*(\d+)\s*:\s*(.+)$", line, re.I)
        if m:
            d["why"].append((int(m.group(1)), m.group(2).strip()))
            continue
        m = re.match(r"^\s*evidence\s*:\s*(.+)$", line, re.I)
        if m:
            d["evidence"].append(m.group(1).strip())
    return d


def check(text):
    d = parse(text)
    out = []
    for k in ("problem", "root cause", "fix", "measure"):
        if not d.get(k):
            out.append(f"no {k.title()}")
    if d.get("problem") and not re.search(r"\d", d["problem"]):
        out.append("Problem has no number: how big, how often, since when?")
    whys = d["why"]
    if [n for n, _ in whys] != list(range(1, len(whys) + 1)):
        out.append("whys are not numbered 1, 2, 3 in order")
    if len(whys) < 3:
        out.append(f"{len(whys)} why(s): stopped too early, usually a symptom")
    if len(whys) > 7:
        out.append(f"{len(whys)} whys: drifting; go back and check the evidence")
    for n, w in whys:
        low = w.lower()
        for b in BLAME:
            if b in low:
                out.append(f"Why {n} blames a person ('{b}'): ask why the process allowed it")
                break
        if not low.startswith("because") and "because" not in low:
            out.append(f"Why {n} is not a 'because' answer")
    if len(d["evidence"]) < max(1, len(whys) - 1):
        out.append(f"{len(d['evidence'])} piece(s) of evidence for {len(whys)} whys: each link needs something you can check")
    rc = d.get("root cause", "")
    if rc and whys:
        best = max(len(toks(rc) & toks(w)) / max(1, len(toks(rc))) for _, w in whys[-2:])
        if best < 0.3:
            out.append("Root cause does not follow from the last two whys")
    if rc and d.get("problem"):
        a, b = toks(rc), toks(d["problem"])
        if a and len(a & b) / len(a) >= 0.6:
            out.append("Root cause just restates the problem")
    fx = d.get("fix", "").lower()
    for w in WEAK_FIX:
        if w in fx:
            out.append(f"Fix ('{w}') changes behaviour, not the process: people will forget again")
            break
    return out


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    found = check(text)
    print("\n".join(found) if found else "Root cause write-up OK.")
    sys.exit(1 if found else 0)

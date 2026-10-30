#!/usr/bin/env python3
"""Check a business glossary, and optionally scan a document for terms it says to avoid.

CSV columns: term,definition,avoid,example,non_example,owner
avoid: words that mean the same thing but must not be used, separated by ;
Usage: glossary.py glossary.csv [--scan document.txt]
"""
import csv
import re
import sys

STOP = {"a", "an", "the", "of", "is", "are", "to", "for", "and", "or", "in", "who", "that", "which", "this", "it", "has", "have", "with", "by", "on"}


def words(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP}


def check(rows):
    out, terms, avoid_of = [], {}, {}
    for r in rows:
        t = (r.get("term") or "").strip()
        if not t:
            out.append("a row has no term")
            continue
        key = t.lower().rstrip("s")
        if key in terms:
            out.append(f"{t}: defined twice (also as '{terms[key]}')")
        terms[key] = t
        d = (r.get("definition") or "").strip()
        if len(d.split()) < 6:
            out.append(f"{t}: definition is too short to settle an argument")
        elif words(d) <= words(t) | {"customer", "person", "record"}:
            out.append(f"{t}: the definition only repeats the term")
        elif re.match(rf"^\s*(a|an|the)?\s*{re.escape(t.lower())}\b", d.lower()):
            out.append(f"{t}: the definition starts with the term it defines")
        if re.search(r"\b(etc|and so on|various|stuff|things like)\b", d.lower()):
            out.append(f"{t}: the definition is open-ended")
        for col in ("example", "non_example"):
            if not (r.get(col) or "").strip():
                out.append(f"{t}: no {col.replace('_', '-')}: a boundary needs one on each side")
        if not (r.get("owner") or "").strip():
            out.append(f"{t}: no owner to settle disputes")
        for a in [x.strip().lower() for x in (r.get("avoid") or "").split(";") if x.strip()]:
            avoid_of.setdefault(a, []).append(t)
    for a, owners in avoid_of.items():
        if a.rstrip("s") in terms:
            out.append(f"'{a}' is on the avoid list for {', '.join(owners)} but is also a glossary term: pick one")
    return out, avoid_of


def scan(text, avoid_of):
    found = []
    for word, owners in sorted(avoid_of.items()):
        n = len(re.findall(rf"\b{re.escape(word)}s?\b", text, re.I))
        if n:
            found.append(f"'{word}' appears {n} time{'s' if n > 1 else ''}; the glossary says use '{owners[0]}'")
    return found


if __name__ == "__main__":
    args = sys.argv[1:]
    doc = None
    if "--scan" in args:
        i = args.index("--scan")
        doc = open(args[i + 1]).read()
        del args[i:i + 2]
    with open(args[0], newline="") as f:
        problems, avoid_of = check(list(csv.DictReader(f)))
    if doc is not None:
        problems += scan(doc, avoid_of)
    print("\n".join(problems) if problems else "Glossary OK.")
    sys.exit(1 if problems else 0)

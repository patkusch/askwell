#!/usr/bin/env python3
"""Find likely conflicts in a requirements list.

CSV columns: id,text.  Optional: --terms terms.json, e.g.
{"customer": ["client", "account holder"]}
Reports near-duplicates, same-thing-different-number pairs, shall vs shall not
pairs, and inconsistent use of terms. These are leads to check, not verdicts.
"""
import csv
import json
import re
import sys
from itertools import combinations

STOP = {"the", "a", "an", "of", "to", "and", "or", "in", "on", "for", "by", "be", "is", "are",
        "shall", "must", "will", "with", "within", "at", "than", "that", "it", "any", "all"}
NUM = re.compile(r"\d[\d,]*\.?\d*")


def toks(text):
    return {w for w in re.findall(r"[a-z]+", NUM.sub(" ", text.lower())) if w not in STOP}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def numbers(text):
    return [n.replace(",", "") for n in NUM.findall(text)]


def find(rows, terms=None):
    out = []
    info = [(r["id"], r["text"], toks(r["text"]), numbers(r["text"])) for r in rows]
    for (ia, ta, wa, na), (ib, tb, wb, nb) in combinations(info, 2):
        sim = jaccard(wa, wb)
        if sim >= 0.6 and na and nb and na != nb:
            out.append(("number clash", ia, ib, f"same subject, different numbers {na} vs {nb}"))
        elif sim >= 0.8:
            out.append(("duplicate", ia, ib, "say nearly the same thing: merge"))
        neg_a, neg_b = bool(re.search(r"\b(shall|must) not\b", ta.lower())), bool(re.search(r"\b(shall|must) not\b", tb.lower()))
        if sim >= 0.5 and neg_a != neg_b:
            out.append(("opposite", ia, ib, "one says must, the other must not"))
    for preferred, variants in (terms or {}).items():
        names = [preferred] + variants
        used = {}
        for rid, text, _, _ in info:
            for n in names:
                if re.search(rf"\b{re.escape(n)}s?\b", text.lower()):
                    used.setdefault(n, []).append(rid)
        if len(used) > 1:
            detail = "; ".join(f"'{n}' in {', '.join(ids)}" for n, ids in used.items())
            out.append(("term drift", "", "", f"one thing, several names: {detail}"))
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    terms = None
    if "--terms" in args:
        i = args.index("--terms")
        terms = json.load(open(args[i + 1]))
        del args[i:i + 2]
    with open(args[0], newline="") as f:
        found = find(list(csv.DictReader(f)), terms)
    for kind, a, b, why in found:
        print(f"{kind}: {a} {b} - {why}".replace("  ", " "))
    print("No likely conflicts." if not found else f"{len(found)} lead(s) to check.")
    sys.exit(1 if found else 0)

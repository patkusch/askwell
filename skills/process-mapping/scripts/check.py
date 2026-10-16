#!/usr/bin/env python3
"""Check a Mermaid flowchart for structural mistakes.

Finds: no start or several starts, steps that go nowhere, decisions with fewer
than two exits or unlabeled exits, steps not reachable from the start.
Stadium-shaped nodes  A([text])  count as start/end points.
"""
import re
import sys

ARROW = re.compile(r"\s*(-->\|[^|]*\||-->|---|-\.->|==>)\s*")
NODE = re.compile(r"^\s*([A-Za-z_][\w]*)\s*(\(\[.*\]\)|\[.*\]|\{.*\}|\(.*\)|\[\[.*\]\])?\s*$")
SKIP = ("flowchart", "graph", "subgraph", "end", "%%", "classdef", "class ", "style ", "direction", "click")


def parse(text):
    shapes, edges = {}, []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.lower().startswith(SKIP) or line == "end":
            continue
        line = re.sub(r"--\s+([^->|]+?)\s+-->", r"-->|\1|", line)
        parts = ARROW.split(line)
        ids = []
        for p in parts[::2]:
            m = NODE.match(p)
            if not m:
                continue
            nid, shape = m.group(1), m.group(2)
            if shape:
                shapes[nid] = "stadium" if shape.startswith("([") else "decision" if shape.startswith("{") else "step"
            else:
                shapes.setdefault(nid, "step")
            ids.append(nid)
        arrows = parts[1::2]
        for i, a in enumerate(arrows):
            if i + 1 < len(ids):
                label = a[4:-1] if a.startswith("-->|") else ""
                edges.append((ids[i], ids[i + 1], label.strip()))
    return shapes, edges


def check(text):
    shapes, edges = parse(text)
    if not shapes:
        return ["no nodes found: is this a Mermaid flowchart?"]
    out_e = {n: [e for e in edges if e[0] == n] for n in shapes}
    in_e = {n: [e for e in edges if e[1] == n] for n in shapes}
    problems = []
    starts = [n for n in shapes if not in_e[n]]
    if not starts:
        problems.append("no start: every step has something pointing at it")
    elif len(starts) > 1:
        problems.append(f"{len(starts)} starting points ({', '.join(starts)}): one trigger per process, or something is not connected")
    for n, shape in shapes.items():
        if not out_e[n] and shape != "stadium":
            problems.append(f"{n}: dead end. Add the next step or mark it as an end with ([ ])")
        if shape == "decision":
            if len(out_e[n]) < 2:
                problems.append(f"{n}: decision with {len(out_e[n])} exit(s); needs at least 2")
            for _, t, lab in out_e[n]:
                if not lab:
                    problems.append(f"{n} -> {t}: decision exit has no label (Yes / No)")
    if starts:
        seen, stack = set(), [starts[0]]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack += [t for _, t, _ in out_e[cur]]
        if len(starts) == 1:
            for n in shapes:
                if n not in seen:
                    problems.append(f"{n}: cannot be reached from the start")
    return problems


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    text = re.sub(r"^```(mermaid)?\s*$", "", text, flags=re.M)
    found = check(text)
    print("\n".join(found) if found else "Process structure OK.")
    sys.exit(1 if found else 0)

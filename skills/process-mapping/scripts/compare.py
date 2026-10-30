#!/usr/bin/env python3
"""Compare an as-is and a to-be Mermaid flowchart and say whether the to-be is simpler.

Counts steps, decisions, handoffs (an arrow that crosses from one swimlane
subgraph to another), loops (arrows that go back) and the longest path from the start.
Fewer is better on each. Exit 1 if the to-be is worse on any measure.
Usage: compare.py as_is.mmd to_be.mmd
"""
import re
import sys

ARROW = re.compile(r"\s*(-->\|[^|]*\||-->|---|-\.->|==>)\s*")
NODE = re.compile(r"^\s*([A-Za-z_][\w]*)\s*(\(\[(.*)\]\)|\[(.*)\]|\{(.*)\}|\((.*)\))?\s*$")


def parse(text):
    shapes, labels, lane_of, edges = {}, {}, {}, []
    lane = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("%%", "flowchart", "graph", "classDef", "class ", "style ", "direction")):
            continue
        if line.lower().startswith("subgraph"):
            lane = line[8:].strip().strip('"') or "lane"
            lane = re.sub(r"\s*\[.*\]$", "", lane)
            continue
        if line == "end":
            lane = None
            continue
        line = re.sub(r"--\s+([^->|]+?)\s+-->", r"-->|\1|", line)
        parts = ARROW.split(line)
        ids = []
        for p in parts[::2]:
            m = NODE.match(p)
            if not m:
                continue
            nid = m.group(1)
            if m.group(2):
                shapes[nid] = "end" if m.group(2).startswith("([") else "decision" if m.group(2).startswith("{") else "step"
                labels[nid] = (m.group(3) or m.group(4) or m.group(5) or m.group(6) or nid).strip()
            else:
                shapes.setdefault(nid, "step")
                labels.setdefault(nid, nid)
            if lane and nid not in lane_of:
                lane_of[nid] = lane
            ids.append(nid)
        for i in range(len(parts[1::2])):
            if i + 1 < len(ids):
                edges.append((ids[i], ids[i + 1]))
    return shapes, labels, lane_of, edges


def measures(text):
    shapes, labels, lane_of, edges = parse(text)
    succ = {n: [] for n in shapes}
    for a, b in edges:
        succ.setdefault(a, []).append(b)
    has_in = {b for _, b in edges}
    starts = [n for n in shapes if n not in has_in] or list(shapes)[:1]
    # longest path from the start, ignoring arrows that go back; each back arrow is one loop
    loops = 0
    state, best = {}, {}

    def walk(n):
        nonlocal loops
        state[n] = 1
        longest_below = 0
        for m in succ.get(n, []):
            if state.get(m) == 1:
                loops += 1
            else:
                if m not in best:
                    walk(m)
                longest_below = max(longest_below, best[m])
        state[n] = 2
        best[n] = 1 + longest_below

    longest = 0
    if starts:
        walk(starts[0])
        longest = best[starts[0]]
    handoffs = sum(1 for a, b in edges if lane_of.get(a) and lane_of.get(b) and lane_of[a] != lane_of[b])
    return {
        "steps": sum(1 for s in shapes.values() if s == "step"),
        "decisions": sum(1 for s in shapes.values() if s == "decision"),
        "handoffs": handoffs,
        "loops": loops,
        "longest path": longest,
    }, {labels[n].lower() for n, s in shapes.items() if s == "step"}


def compare(as_is, to_be):
    a, a_steps = measures(as_is)
    b, b_steps = measures(to_be)
    worse = [k for k in a if b[k] > a[k]]
    return a, b, worse, sorted(a_steps - b_steps), sorted(b_steps - a_steps)


if __name__ == "__main__":
    a, b, worse, removed, added = compare(open(sys.argv[1]).read(), open(sys.argv[2]).read())
    print(f"{'measure'.ljust(14)}{'as-is'.rjust(7)}{'to-be'.rjust(7)}")
    for k in a:
        mark = "  worse" if k in worse else ""
        print(f"{k.ljust(14)}{str(a[k]).rjust(7)}{str(b[k]).rjust(7)}{mark}")
    if removed:
        print("Steps removed: " + "; ".join(removed))
    if added:
        print("Steps added: " + "; ".join(added))
    if worse:
        print("The to-be is worse on: " + ", ".join(worse) + ". Say why that is worth it, or simplify.")
    else:
        print("The to-be is no worse on any measure.")
    sys.exit(1 if worse else 0)

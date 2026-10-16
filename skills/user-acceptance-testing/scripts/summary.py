#!/usr/bin/env python3
"""Summarise UAT results and give a go / go with conditions / no-go call.

scenarios.csv: id,requirement,scenario,result,defect_id    result: pass|fail|blocked|not run
defects.csv:   defect_id,severity,status,kind               severity: critical|major|minor
                                                            status: open|fixed|closed|accepted
                                                            kind: defect|change request
Optional: --requirements matrix.csv (column req_id) to find requirements nobody tested.
Rules: any open critical/major defect, or any scenario not passed, is a no-go.
Open minor defects give "go with conditions". Change requests do not block a go.
"""
import csv
import sys

OPEN = {"open", "reopened", "in progress"}


def evaluate(scenarios, defects, requirements=None):
    problems, notes = [], []
    dmap = {}
    for d in defects:
        did = (d.get("defect_id") or "").strip()
        if did in dmap:
            problems.append(f"{did}: defect listed twice")
        dmap[did] = d
    counts = {"pass": 0, "fail": 0, "blocked": 0, "not run": 0}
    for s in scenarios:
        res = (s.get("result") or "").strip().lower()
        sid = s.get("id", "?")
        if res not in counts:
            problems.append(f"{sid}: result must be pass, fail, blocked or not run")
            continue
        counts[res] += 1
        did = (s.get("defect_id") or "").strip()
        if res == "fail" and not did:
            problems.append(f"{sid}: failed with no defect logged")
        if did and did not in dmap:
            problems.append(f"{sid}: points at {did}, which is not in the defect list")
        if res == "pass" and did in dmap and (dmap[did].get("status") or "").strip().lower() in OPEN \
                and (dmap[did].get("kind") or "defect").strip().lower() == "defect":
            problems.append(f"{sid}: marked pass but {did} is still open")
    blocking, minor = [], []
    for did, d in dmap.items():
        if (d.get("status") or "").strip().lower() not in OPEN:
            continue
        if (d.get("kind") or "defect").strip().lower() == "change request":
            notes.append(f"{did}: open change request: handle outside UAT sign-off")
            continue
        sev = (d.get("severity") or "").strip().lower()
        if sev in {"critical", "major"}:
            blocking.append(f"{did} ({sev})")
        elif sev == "minor":
            minor.append(did)
        else:
            problems.append(f"{did}: severity must be critical, major or minor")
    if requirements is not None:
        tested = {(s.get("requirement") or "").strip() for s in scenarios}
        for r in requirements:
            if r not in tested:
                problems.append(f"{r}: no UAT scenario covers this requirement")
    not_passed = counts["fail"] + counts["blocked"] + counts["not run"]
    if blocking or not_passed or problems:
        call = "NO-GO"
    elif minor:
        call = "GO WITH CONDITIONS"
    else:
        call = "GO"
    return {"call": call, "counts": counts, "blocking": blocking, "minor_open": minor,
            "problems": problems, "notes": notes}


if __name__ == "__main__":
    args = sys.argv[1:]
    reqs = None
    if "--requirements" in args:
        i = args.index("--requirements")
        with open(args[i + 1], newline="") as f:
            reqs = [r["req_id"].strip() for r in csv.DictReader(f)]
        del args[i:i + 2]
    with open(args[0], newline="") as f:
        sc = list(csv.DictReader(f))
    with open(args[1], newline="") as f:
        df = list(csv.DictReader(f))
    r = evaluate(sc, df, reqs)
    c = r["counts"]
    print(f"{r['call']}: {c['pass']} passed, {c['fail']} failed, {c['blocked']} blocked, {c['not run']} not run")
    if r["blocking"]:
        print("Open critical/major: " + ", ".join(r["blocking"]))
    if r["minor_open"]:
        print("Open minor (accept with owner and date): " + ", ".join(r["minor_open"]))
    for p in r["problems"] + r["notes"]:
        print("  " + p)
    sys.exit(0 if r["call"] == "GO" else 1)

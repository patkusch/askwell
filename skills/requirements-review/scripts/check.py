#!/usr/bin/env python3
"""Check the records of a requirements review: findings quoted, double-checked and accounted for.

Usage: check.py review_findings.json review_requirements.csv review_coverage.csv [--report]

review_requirements.csv   columns id,text: the requirements under review.
review_findings.json      a list of findings. Each has id, kind, verdict, requirements,
                          quotes, what, found_by, checked_by, and then by verdict:
                            confirmed     impact, severity (high, medium, low), who_decides
                            needs-answer  open_question, who_can_answer
                            rejected      reason
review_coverage.csv       one row per requirement, one column per pass. A cell holds
                          clear, one or more finding ids, or "skipped: why".

It checks the records, not the judgement: that each quote is in the requirement word
for word, that a second person or agent checked each finding, that nothing is rated
before it is confirmed, and that every requirement was looked at in every pass.
--report prints the review report, and only when the records pass.
"""
import csv
import json
import sys

PASSES = ["contradiction", "duplicate", "hidden-conflict", "number-mismatch",
          "term-drift", "gap", "ownership", "scope-leak"]
NEED_TWO = {"contradiction", "duplicate", "hidden-conflict", "number-mismatch", "term-drift"}
VERDICTS = ("confirmed", "needs-answer", "rejected")
SEVERITIES = ("high", "medium", "low")


def squash(text):
    return " ".join(str(text).lower().split())


def val(rec, key):
    return str(rec.get(key) or "").strip()


def req_list(f):
    r = f.get("requirements")
    return [str(x).strip() for x in r] if isinstance(r, list) else []


def first_by_id(findings):
    out = {}
    for f in findings:
        if val(f, "id") and val(f, "id") not in out:
            out[val(f, "id")] = f
    return out


def check_findings(findings, reqs):
    problems = []
    seen = set()
    same = {}
    for n, f in enumerate(findings, 1):
        if not isinstance(f, dict):
            problems.append(f"finding {n}: not a record")
            continue
        fid = val(f, "id")
        if not fid:
            fid = f"finding {n}"
            problems.append(f"{fid}: no id")
        elif fid in seen:
            problems.append(f"{fid}: id used twice")
        seen.add(fid)

        kind, verdict = val(f, "kind"), val(f, "verdict")
        if kind not in PASSES:
            problems.append(f"{fid}: kind '{kind}' is not one of the eight passes")
        if not val(f, "what"):
            problems.append(f"{fid}: does not say what is wrong")

        ids = req_list(f)
        if kind in NEED_TWO and len(ids) < 2:
            problems.append(f"{fid}: a {kind} needs two requirements, names {len(ids)}")
        elif not ids:
            problems.append(f"{fid}: names no requirement")
        quotes = f.get("quotes") if isinstance(f.get("quotes"), dict) else {}
        for rid in ids:
            if rid not in reqs:
                problems.append(f"{fid}: names {rid}, which is not in the requirements")
            elif not str(quotes.get(rid) or "").strip():
                problems.append(f"{fid}: no quote from {rid}")
            elif squash(quotes[rid]) not in squash(reqs[rid]):
                problems.append(f"{fid}: the quote from {rid} is not in {rid} word for word")
        if kind in PASSES and ids:
            key = (kind, frozenset(ids))
            if key in same:
                problems.append(f"{fid}: same kind and same requirements as {same[key]}, so one finding is recorded twice")
            else:
                same[key] = fid

        finder, checker = val(f, "found_by"), val(f, "checked_by")
        if not finder:
            problems.append(f"{fid}: no finder named")
        if not checker:
            problems.append(f"{fid}: no second reviewer named")
        elif finder and squash(finder) == squash(checker):
            problems.append(f"{fid}: found and checked by the same reviewer ({finder})")

        if verdict not in VERDICTS:
            problems.append(f"{fid}: verdict '{verdict}' is not confirmed, needs-answer or rejected")
        elif verdict == "confirmed":
            if not val(f, "impact"):
                problems.append(f"{fid}: confirmed but does not say what goes wrong if it is left")
            if val(f, "severity").lower() not in SEVERITIES:
                problems.append(f"{fid}: severity '{val(f, 'severity')}' is not high, medium or low")
            if not val(f, "who_decides"):
                problems.append(f"{fid}: confirmed but no one is named to decide")
        else:
            if val(f, "severity"):
                problems.append(f"{fid}: has a severity but is not confirmed")
            if verdict == "needs-answer":
                if not val(f, "open_question").endswith("?"):
                    problems.append(f"{fid}: needs an answer but does not ask a question")
                if not val(f, "who_can_answer"):
                    problems.append(f"{fid}: no one is named who can answer")
            elif not val(f, "reason"):
                problems.append(f"{fid}: rejected without a reason")
    return problems


def check_coverage(rows, columns, findings, reqs):
    problems = [f"coverage sheet has no column for {p}" for p in PASSES if p not in columns]
    by_id = first_by_id([f for f in findings if isinstance(f, dict)])
    listed, shown = set(), set()
    for row in rows:
        rid = (row.get("requirement") or "").strip()
        if not rid:
            problems.append("a coverage row names no requirement")
            continue
        if rid in listed:
            problems.append(f"{rid}: listed twice in the coverage sheet")
        listed.add(rid)
        if rid not in reqs:
            problems.append(f"{rid}: in the coverage sheet but not in the requirements")
            continue
        for p in PASSES:
            if p not in columns:
                continue
            cell = (row.get(p) or "").strip()
            low = cell.lower()
            if not cell:
                problems.append(f"{rid}: not checked for {p} (empty cell)")
            elif low == "clear":
                pass
            elif low.startswith("skipped"):
                if not low[len("skipped"):].strip(" :-"):
                    problems.append(f"{rid}: skipped for {p} without a reason")
            else:
                for fid in cell.replace(",", " ").split():
                    f = by_id.get(fid)
                    if f is None:
                        problems.append(f"{rid}: coverage names {fid} under {p}, which is not a finding")
                    elif val(f, "kind") != p or rid not in req_list(f):
                        about = ", ".join(req_list(f)) or "no requirement"
                        problems.append(f"{rid}: coverage puts {fid} under {p}, but {fid} is a {val(f, 'kind')} finding about {about}")
                    else:
                        shown.add((fid, rid))
    for rid in reqs:
        if rid not in listed:
            problems.append(f"{rid}: not in the coverage sheet, so it was never reviewed")
    for fid, f in by_id.items():
        kind = val(f, "kind")
        if kind in columns and kind in PASSES:
            for rid in req_list(f):
                if rid in listed and rid in reqs and (fid, rid) not in shown:
                    problems.append(f"{fid}: the coverage sheet does not show it under {kind} for {rid}")
    return problems


def check(findings, reqs, rows, columns):
    """Every problem in the review records, as plain lines. An empty list means they hold up."""
    if not isinstance(findings, list):
        return ["the findings file must be a list of findings"]
    return check_findings(findings, reqs) + check_coverage(rows, columns, findings, reqs)


def skipped(rows, columns):
    """What was not looked at: {(pass, reason): [requirement ids]}."""
    out = {}
    for row in rows:
        for p in PASSES:
            cell = (row.get(p) or "").strip() if p in columns else ""
            if cell.lower().startswith("skipped"):
                out.setdefault((p, cell[len("skipped"):].strip(" :-")), []).append(row["requirement"].strip())
    return out


def counts(findings):
    return {v: sum(1 for f in findings if val(f, "verdict") == v) for v in VERDICTS}


def cell(text):
    return str(text).replace("|", "/").replace("\n", " ").strip()


def report(findings, reqs, rows, columns):
    """The review report, written only from the records."""
    c = counts(findings)
    out = ["# Requirements review", "",
           f"{len(reqs)} requirements reviewed in {len(PASSES)} passes. {c['confirmed']} confirmed, "
           f"{c['needs-answer']} waiting for an answer, {c['rejected']} raised and rejected.", ""]

    def table(title, head, picked, cols):
        if not picked:
            return
        out.extend([f"## {title}", "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)])
        for f in picked:
            out.append("| " + " | ".join(cell(col(f)) for col in cols) + " |")
        out.append("")

    ids = lambda f: ", ".join(req_list(f))
    confirmed = sorted((f for f in findings if val(f, "verdict") == "confirmed"),
                       key=lambda f: SEVERITIES.index(val(f, "severity").lower()))
    table("Confirmed", ["Finding", "Requirements", "What is wrong", "What goes wrong if it is left", "How bad", "Who decides"],
          confirmed, [lambda f: val(f, "id"), ids, lambda f: val(f, "what"), lambda f: val(f, "impact"),
                      lambda f: val(f, "severity").lower(), lambda f: val(f, "who_decides")])
    table("Waiting for an answer", ["Finding", "Requirements", "Question", "Who can answer"],
          [f for f in findings if val(f, "verdict") == "needs-answer"],
          [lambda f: val(f, "id"), ids, lambda f: val(f, "open_question"), lambda f: val(f, "who_can_answer")])
    table("Raised and rejected", ["Finding", "Requirements", "What was claimed", "Why it was rejected"],
          [f for f in findings if val(f, "verdict") == "rejected"],
          [lambda f: val(f, "id"), ids, lambda f: val(f, "what"), lambda f: val(f, "reason")])
    gaps = skipped(rows, columns)
    if gaps:
        out.extend(["## Not looked at", ""])
        for (p, why), rids in gaps.items():
            out.append(f"- {p}: {', '.join(rids)} ({why})")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def load(findings_path, reqs_path, coverage_path):
    with open(findings_path) as f:
        findings = json.load(f)
    with open(reqs_path, newline="") as f:
        reqs = {(r.get("id") or "").strip(): r.get("text") or "" for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    with open(coverage_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = [c.strip() for c in (reader.fieldnames or [])]
    return findings, reqs, rows, columns


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--report"]
    if len(args) != 3:
        print("Usage: check.py review_findings.json review_requirements.csv review_coverage.csv [--report]", file=sys.stderr)
        sys.exit(2)
    findings, reqs, rows, columns = load(*args)
    problems = check(findings, reqs, rows, columns)
    if problems:
        print("\n".join(problems))
        print(f"{len(problems)} problem(s) in the review records." + (" No report written: fix the records first." if "--report" in sys.argv else ""))
        sys.exit(1)
    if "--report" in sys.argv:
        print(report(findings, reqs, rows, columns), end="")
    else:
        c = counts(findings)
        n = sum(len(v) for v in skipped(rows, columns).values())
        print(f"Review records hold up: {c['confirmed']} confirmed, {c['needs-answer']} waiting for an answer, "
              f"{c['rejected']} rejected, {len(reqs)} requirements covered" + (f", {n} cell(s) skipped with a reason." if n else "."))
    sys.exit(0)

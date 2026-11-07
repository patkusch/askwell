#!/usr/bin/env python3
"""Check the records of a requirements review: findings quoted, double-checked and accounted for.

Usage: check.py review_findings.json review_requirements.csv review_coverage.csv [--report]
                [--previous review_previous.json]
       check.py --start review_requirements.csv      prints an empty coverage sheet to fill in
       check.py --brief review_findings.json review_requirements.csv [F3]
                                                     prints what the second reviewer may see

review_requirements.csv   columns id,text: the requirements under review, each id once.
review_findings.json      a list of findings. Each has id, kind, verdict, requirements,
                          quotes, what, found_by, checked_by, and then by verdict:
                            confirmed     why_it_stands, impact, severity (high, medium,
                                          low), who_decides
                            needs-answer  why_it_stands, open_question, who_can_answer
                            rejected      reason, or same_as (the id of the finding that
                                          records the same problem under another pass)
review_coverage.csv       one row per requirement, one column per pass. A cell holds
                          clear, one or more finding ids, "see F1" for a problem that
                          is recorded under another pass, or "skipped: why".

--previous takes the findings file of an earlier review of the same requirements. A
finding it rejected must still be on record, and may come back under another verdict
only with a what_changed line. A question it left open must still be on record.

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


NOBODY = {"tbd", "tbc", "unknown", "not known", "n/a", "na", "none", "nobody", "someone", "anyone",
          "to be decided", "to be confirmed", "to be agreed"}


def check_findings(findings, reqs):
    problems = []

    def named(fid, f, key):
        """True if the field is filled in. A placeholder counts as filled in, and is reported."""
        if val(f, key) and squash(val(f, key)).strip(" .?!-") in NOBODY | {""}:
            problems.append(f"{fid}: '{val(f, key)}' names nobody: give a person or the role that is needed")
        return bool(val(f, key))

    seen = set()
    same = {}
    by_id = first_by_id([f for f in findings if isinstance(f, dict)])
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
        for rid in sorted({r for r in ids if ids.count(r) > 1}):
            problems.append(f"{fid}: names {rid} twice")
        ids = list(dict.fromkeys(ids))
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
            elif kind != "term-drift" and len(str(quotes[rid]).split()) < 2:
                problems.append(f"{fid}: the quote from {rid} is one word, too short to show anything")
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
            if not named(fid, f, "who_decides"):
                problems.append(f"{fid}: confirmed but no one is named to decide")
        else:
            if val(f, "severity"):
                problems.append(f"{fid}: has a severity but is not confirmed")
            if verdict == "needs-answer":
                if not val(f, "open_question").endswith("?"):
                    problems.append(f"{fid}: needs an answer but does not ask a question")
                elif val(f, "open_question").count("?") > 1:
                    problems.append(f"{fid}: asks more than one question; one exact fact per finding")
                if not named(fid, f, "who_can_answer"):
                    problems.append(f"{fid}: no one is named who can answer")
                elif squash(val(f, "who_can_answer")) in {squash(finder), squash(checker)} - {""}:
                    problems.append(f"{fid}: the reviewer who asked cannot be the one who answers ({val(f, 'who_can_answer')})")
            elif not val(f, "reason") and not val(f, "same_as"):
                problems.append(f"{fid}: rejected without a reason")
        if verdict in ("confirmed", "needs-answer") and not val(f, "why_it_stands"):
            problems.append(f"{fid}: the second reviewer does not say why it stands")
        twin = val(f, "same_as")
        if twin and verdict in VERDICTS and verdict != "rejected":
            problems.append(f"{fid}: says it is the same problem as {twin} but is not rejected")
        elif twin and (twin == fid or val(by_id.get(twin, {}), "verdict") not in ("confirmed", "needs-answer")):
            problems.append(f"{fid}: says it is the same problem as {twin}, but {twin} is not a finding that stands")
    return problems


def check_coverage(rows, columns, findings, reqs):
    problems = [f"coverage sheet has no column for {p}" for p in PASSES if p not in columns]
    for c in columns:
        if c not in PASSES and c != "requirement":
            problems.append(f"coverage sheet has a column '{c}' that is not a pass")
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
                see = low.startswith("see ")  # the pass turned up a problem already recorded under another pass
                for fid in (cell[4:] if see else cell).replace(",", " ").split():
                    f = by_id.get(fid)
                    if f is None:
                        problems.append(f"{rid}: coverage names {fid} under {p}, which is not a finding")
                    elif rid not in req_list(f) or (val(f, "kind") != p and not see):
                        about = ", ".join(req_list(f)) or "no requirement"
                        problems.append(f"{rid}: coverage puts {fid} under {p}, but {fid} is filed as {val(f, 'kind')}, about {about}")
                    elif not see:
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


def check_requirements(pairs):
    """Turn (id, text) rows into {id: text}, and say what is wrong with the list itself."""
    problems, reqs = [], {}
    for rid, text in pairs:
        if rid in reqs:
            problems.append(f"{rid}: listed twice in the requirements")
            continue
        reqs[rid] = text
        if not text.strip():
            problems.append(f"{rid}: has no text to review")
    return reqs, problems


def check_previous(previous, findings, reqs):
    """Nothing an earlier review settled or left open may quietly change or vanish."""
    problems = []
    now = {}
    for f in findings:
        if isinstance(f, dict):
            now.setdefault((val(f, "kind"), frozenset(req_list(f))), f)
    for e in previous if isinstance(previous, list) else []:
        if not isinstance(e, dict) or val(e, "verdict") not in ("rejected", "needs-answer"):
            continue
        ids = req_list(e)
        if not ids or any(rid not in reqs for rid in ids):
            continue  # a requirement it was about is gone, so there is nothing to carry over
        eid = val(e, "id") or "a finding"
        cur = now.get((val(e, "kind"), frozenset(ids)))
        if cur is None and val(e, "verdict") == "rejected":
            problems.append(f"earlier {eid}: was rejected and is missing here, so it can be raised again")
        elif cur is None:
            problems.append(f"earlier {eid}: was waiting for an answer and is missing here")
        elif val(e, "verdict") == "rejected" and val(cur, "verdict") != "rejected" and not val(cur, "what_changed"):
            problems.append(f"{val(cur, 'id') or 'a finding'}: the earlier review rejected this as {eid}, and it does not say what changed")
    return problems


def check(findings, reqs, rows, columns, previous=None):
    """Every problem in the review records, as plain lines. An empty list means they hold up.

    reqs is {id: text}, or the (id, text) rows as read from the file.
    previous is the findings list of an earlier review, if there was one.
    """
    if not isinstance(findings, list):
        return ["the findings file must be a list of findings"]
    reqs, problems = (reqs, []) if isinstance(reqs, dict) else check_requirements(reqs)
    problems += check_findings(findings, reqs) + check_coverage(rows, columns, findings, reqs)
    return problems + (check_previous(previous, findings, reqs) if previous is not None else [])


def skipped(rows, columns):
    """What was not looked at: {(pass, reason): [requirement ids]}."""
    out = {}
    for row in rows:
        for p in PASSES:
            cell = (row.get(p) or "").strip() if p in columns else ""
            if cell.lower().startswith("skipped"):
                out.setdefault((p, cell[len("skipped"):].strip(" :-")), []).append(row["requirement"].strip())
    return out


def tally(rows, columns):
    """How many requirement-and-pass checks came out clear, with a finding, or skipped."""
    t = {"clear": 0, "finding": 0, "skipped": 0}
    for row in rows:
        for p in PASSES:
            low = (row.get(p) or "").strip().lower() if p in columns else ""
            t["clear" if low == "clear" else "skipped" if low.startswith("skipped") else "finding"] += 1
    return t


def counts(findings):
    return {v: sum(1 for f in findings if val(f, "verdict") == v) for v in VERDICTS}


def cell(text):
    return str(text).replace("|", "/").replace("\n", " ").strip()


def report(findings, reqs, rows, columns):
    """The review report, written only from the records."""
    reqs = dict(reqs)
    c, t = counts(findings), tally(rows, columns)
    out = ["# Requirements review", "",
           f"{len(reqs)} requirements reviewed in {len(PASSES)} passes. {c['confirmed']} confirmed, "
           f"{c['needs-answer']} waiting for an answer, {c['rejected']} raised and rejected.", "",
           f"{sum(t.values())} checks (each requirement in each pass): {t['clear']} clear, "
           f"{t['finding']} with a finding, {t['skipped']} skipped.", ""]

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
    if confirmed:
        out.extend(["The words each confirmed finding rests on:", ""])
        for f in confirmed:
            out.extend(f"- {val(f, 'id')}, {rid}: \"{' '.join(str(f['quotes'][rid]).split())}\"" for rid in req_list(f))
        out.append("")
    table("Waiting for an answer", ["Finding", "Requirements", "Question", "Who can answer"],
          [f for f in findings if val(f, "verdict") == "needs-answer"],
          [lambda f: val(f, "id"), ids, lambda f: val(f, "open_question"), lambda f: val(f, "who_can_answer")])
    table("Raised and rejected", ["Finding", "Requirements", "What was claimed", "Why it was rejected"],
          [f for f in findings if val(f, "verdict") == "rejected"],
          [lambda f: val(f, "id"), ids, lambda f: val(f, "what"),
           lambda f: " ".join(x for x in (f"Same problem as {val(f, 'same_as')}." if val(f, "same_as") else "", val(f, "reason")) if x)])
    gaps = skipped(rows, columns)
    if gaps:
        out.extend(["## Not looked at", ""])
        for (p, why), rids in gaps.items():
            out.append(f"- {p}: {', '.join(rids)} ({why})")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def read_requirements(path):
    with open(path, newline="") as f:
        return [((r.get("id") or "").strip(), r.get("text") or "") for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def blank_coverage(reqs):
    """An empty coverage sheet: one row per requirement, one empty cell per pass."""
    lines = [",".join(["requirement"] + PASSES)]
    lines += [rid + "," * len(PASSES) for rid in dict(reqs)]
    return "\n".join(lines) + "\n"


BRIEF = """You did not write this finding. Try to disprove it.
Read each requirement it names in full, not only the quoted words.
For a conflict: is there a reading in which both requirements can be met?
For a gap: is the case really uncovered, or does another requirement cover it?
For two owners: does anything say whose word counts?
Is something missing that only a named person can tell us?
Answer with one verdict: confirmed, needs-answer or rejected, and say why."""


def brief(findings, reqs, only=None):
    """What the second reviewer gets: the claim and the requirements in full. Nothing else.

    The finder's notes, name and any verdict are left out, so the check starts cold.
    """
    reqs = dict(reqs)
    out = []
    for f in findings:
        if not isinstance(f, dict) or (only and val(f, "id") != only):
            continue
        quotes = f.get("quotes") if isinstance(f.get("quotes"), dict) else {}
        out.append(f"{val(f, 'id')} ({val(f, 'kind')}): {val(f, 'what')}")
        for rid in req_list(f):
            out.append(f"  {rid} in full: {reqs.get(rid, '(not in the requirements)')}")
            out.append(f"  {rid} quoted: \"{' '.join(str(quotes.get(rid) or '').split())}\"")
        out.append("")
    return "\n".join([BRIEF, ""] + out) if out else ""


def load(findings_path, reqs_path, coverage_path):
    with open(findings_path) as f:
        findings = json.load(f)
    reqs = read_requirements(reqs_path)
    with open(coverage_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = [c.strip() for c in (reader.fieldnames or [])]
    return findings, reqs, rows, columns


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--start":
        print(blank_coverage(read_requirements(sys.argv[2])), end="")
        sys.exit(0)
    if len(sys.argv) in (4, 5) and sys.argv[1] == "--brief":
        with open(sys.argv[2]) as bf:
            text = brief(json.load(bf), read_requirements(sys.argv[3]), sys.argv[4] if len(sys.argv) == 5 else None)
        print(text or "No such finding.", end="")
        sys.exit(0 if text else 2)
    args = [a for a in sys.argv[1:] if a != "--report"]
    previous = None
    if "--previous" in args[:-1]:
        i = args.index("--previous")
        with open(args[i + 1]) as pf:
            previous = json.load(pf)
        del args[i:i + 2]
    if len(args) != 3:
        print("Usage: check.py review_findings.json review_requirements.csv review_coverage.csv [--report] [--previous review_previous.json]", file=sys.stderr)
        sys.exit(2)
    try:
        findings, reqs, rows, columns = load(*args)
    except (OSError, ValueError) as e:
        print(f"Cannot read the review files: {e}", file=sys.stderr)
        sys.exit(2)
    problems = check(findings, reqs, rows, columns, previous)
    if problems:
        print("\n".join(problems))
        print(f"{len(problems)} problem(s) in the review records." + (" No report written: fix the records first." if "--report" in sys.argv else ""))
        sys.exit(1)
    if "--report" in sys.argv:
        print(report(findings, reqs, rows, columns), end="")
    else:
        c, reqs = counts(findings), dict(reqs)
        n = sum(len(v) for v in skipped(rows, columns).values())
        print(f"Review records hold up: {c['confirmed']} confirmed, {c['needs-answer']} waiting for an answer, "
              f"{c['rejected']} rejected, {len(reqs)} requirements covered" + (f", {n} cell(s) skipped with a reason." if n else "."))
    sys.exit(0)

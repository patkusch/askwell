#!/usr/bin/env python3
"""One command for every check.

  askwell.py list                     show every skill that has a check
  askwell.py run <skill> [args...]    run that skill's check with your files
  askwell.py skills                   list all skills with what they are for
  askwell.py audit <folder> [--today YYYY-MM-DD] [-v]
                                      run every check whose file is in the folder

A skill with more than one script is named skill/script, for example
backlog-prioritisation/score. The exit code is the check's own: 0 is clean.
"""
import difflib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "skills"


def checks():
    found = {}
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        scripts = sorted((d / "scripts").glob("*.py")) if (d / "scripts").is_dir() else []
        for s in scripts:
            key = d.name if len(scripts) == 1 else f"{d.name}/{s.stem}"
            found[key] = s
    return found


def first_line(path):
    m = re.search(r'"""(.*?)(\n|""")', path.read_text(), re.S)
    return m.group(1).strip() if m else ""


def description(skill_dir):
    m = re.search(r"^description:\s*(.+)$", (skill_dir / "SKILL.md").read_text(), re.M)
    return m.group(1).strip() if m else ""


# What a project folder holds. Each row: skill, script, required files, args builder,
# optional extra files and the flag that passes them. {f} is replaced by the folder path.
AUDIT = [
    ("problem-statement", "check", ["problem.txt"], [], {}),
    ("stakeholder-mapping", "check", ["stakeholders.csv"], [], {}),
    ("stakeholder-interview", "check", ["interview.txt"], [], {}),
    ("workshop-facilitation", "check", ["workshop.json"], [], {}),
    ("requirements-elicitation", "check", ["needs.csv"], [], {}),
    ("requirements-writing", "lint", ["requirements.txt"], [], {}),
    ("user-stories", "check", ["stories.txt"], [], {}),
    ("acceptance-criteria", "check", ["criteria.txt"], [], {}),
    ("use-cases", "check", ["usecase.txt"], [], {}),
    ("nonfunctional-requirements", "check", ["nfr.csv"], [], {}),
    ("scope-definition", "check", ["scope.txt"], [], {}),
    ("requirements-conflict-check", "conflicts", ["conflict.csv"], [], {"terms.json": "--terms"}),
    ("requirements-traceability", "check", ["matrix.csv"], [], {"tests.csv": "--tests"}),
    ("brd-writing", "check", ["brd.md"], [], {}),
    ("process-mapping", "check", ["process.mmd"], [], {}),
    ("data-dictionary", "check", ["dictionary.csv"], [], {}),
    ("sql-for-analysis", "check", ["analysis.sql"], [], {}),
    ("kpi-definition", "check", ["kpis.json"], [], {}),
    ("options-analysis", "check", ["options.json"], [], {}),
    ("root-cause-analysis", "check", ["rootcause.txt"], [], {}),
    ("gap-analysis", "check", ["gaps.csv"], [], {}),
    ("raid-log", "raid", ["raid.csv"], [], {}),
    ("decision-log", "check", ["decisions.csv"], [], {}),
    ("change-impact-assessment", "check", ["impact.csv"], [], {}),
    ("user-acceptance-testing", "summary", ["uat_scenarios.csv", "uat_defects.csv"], [], {"uat_requirements.csv": "--requirements"}),
    ("stakeholder-communication", "check", ["summary.txt"], [], {}),
    ("meeting-minutes", "actions", ["notes.txt"], [], {}),
    ("vendor-selection", "score", ["scorecard.json"], [], {}),
    ("business-case", "case", ["case.json"], ["--sensitivity"], {}),
    ("backlog-prioritisation", "score", ["moscow.csv"], [], {}),
    ("ba-start-here", "route", ["request.txt"], [], {}),
]
TAKES_TODAY = {"raid-log", "decision-log"}


def audit(folder, today=None, verbose=False):
    """Run every check that has its file in `folder`. Returns the number that found something."""
    folder = Path(folder)
    if not folder.is_dir():
        print(f"'{folder}' is not a folder.", file=sys.stderr)
        return 2
    found = skipped = clean = 0
    detail = []
    for skill, stem, needs, extra, optional in AUDIT:
        files = [folder / n for n in needs]
        if not all(f.is_file() for f in files):
            skipped += 1
            continue
        script = ROOT / skill / "scripts" / f"{stem}.py"
        args = [sys.executable, str(script)]
        if skill == "backlog-prioritisation":
            args.append("moscow")
        if skill == "ba-start-here":
            args.append(files[0].read_text().strip())
        else:
            args += [str(f) for f in files]
        for name, flag in optional.items():
            if (folder / name).is_file():
                args += [flag, str(folder / name)]
        args += extra
        if skill in TAKES_TODAY and today:
            args += ["--today", today]
        r = subprocess.run(args, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0:
            clean += 1
            if verbose:
                detail.append((skill, out, True))
        else:
            found += 1
            detail.append((skill, out, False))
    print(f"{found} check(s) found something, {clean} clean, {skipped} skipped (no file for them).")
    for skill, out, ok in detail:
        print(f"\n== {skill}" + ("  (clean)" if ok else ""))
        print(out)
    return found


def main(argv):
    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    avail = checks()
    if cmd == "list":
        width = max(len(k) for k in avail)
        for k, p in avail.items():
            print(f"{k.ljust(width)}  {first_line(p)}")
        return 0
    if cmd == "skills":
        for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
            desc = description(d)
            print(f"{d.name}\n    {desc[:150]}{'...' if len(desc) > 150 else ''}")
        return 0
    if cmd == "audit":
        if not rest or rest[0].startswith("-"):
            print("audit needs a folder. Try: askwell.py audit examples/refund-approval/good", file=sys.stderr)
            return 2
        today = rest[rest.index("--today") + 1] if "--today" in rest else None
        return audit(rest[0], today, verbose="-v" in rest)
    if cmd == "run":
        if not rest:
            print("run needs a skill name. Try: askwell.py list", file=sys.stderr)
            return 2
        name = rest[0].strip("/")
        if name not in avail:
            guess = difflib.get_close_matches(name, list(avail), n=3, cutoff=0.4)
            hint = f" Did you mean: {', '.join(guess)}?" if guess else " Try: askwell.py list"
            print(f"No check called '{name}'.{hint}", file=sys.stderr)
            return 2
        return subprocess.call([sys.executable, str(avail[name]), *rest[1:]])
    print(f"Unknown command '{cmd}'. Use list, skills, run or audit.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

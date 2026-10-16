#!/usr/bin/env python3
"""One command for every check.

  askwell.py list                     show every skill that has a check
  askwell.py run <skill> [args...]    run that skill's check with your files
  askwell.py skills                   list all skills with what they are for

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
    print(f"Unknown command '{cmd}'. Use list, skills or run.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

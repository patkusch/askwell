#!/usr/bin/env python3
"""Check every skill has valid front matter and a sensible body."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "skills"
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, m.group(2)


def validate(skill_dir):
    errs = []
    f = skill_dir / "SKILL.md"
    if not f.exists():
        return [f"{skill_dir.name}: no SKILL.md"]
    meta, body = parse(f.read_text())
    if meta is None:
        return [f"{skill_dir.name}: no front matter"]
    name, desc = meta.get("name", ""), meta.get("description", "")
    if name != skill_dir.name:
        errs.append(f"{skill_dir.name}: name '{name}' must match the folder")
    if not NAME.match(name):
        errs.append(f"{skill_dir.name}: name must be lower-case with hyphens")
    if not 80 <= len(desc) <= 1024:
        errs.append(f"{skill_dir.name}: description is {len(desc)} chars, want 80-1024")
    if "use when" not in desc.lower():
        errs.append(f"{skill_dir.name}: description must say 'Use when' so the agent knows when to pick it")
    if len(body.strip().splitlines()) < 15:
        errs.append(f"{skill_dir.name}: body is too thin")
    if len(body.splitlines()) > 500:
        errs.append(f"{skill_dir.name}: body over 500 lines")
    for script in sorted((skill_dir / "scripts").glob("*.py")) if (skill_dir / "scripts").is_dir() else []:
        if f"scripts/{script.name}" not in body:
            errs.append(f"{skill_dir.name}: scripts/{script.name} is not mentioned in SKILL.md")
    for ref in sorted((skill_dir / "references").glob("*.md")) if (skill_dir / "references").is_dir() else []:
        if f"references/{ref.name}" not in body:
            errs.append(f"{skill_dir.name}: references/{ref.name} is not mentioned in SKILL.md")
    return errs


def main():
    dirs = sorted(p for p in ROOT.iterdir() if p.is_dir())
    errs = [e for d in dirs for e in validate(d)]
    print("\n".join(errs) if errs else f"{len(dirs)} skills OK.")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())

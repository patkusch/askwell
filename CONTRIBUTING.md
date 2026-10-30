# Adding to askwell

## A new skill

1. Run `python3 scripts/askwell.py new <name>` to start from a template, or make `skills/<name>/SKILL.md` yourself. The name is lower-case with hyphens and matches the folder.
2. Start with this front matter:

```
---
name: your-skill
description: What it does, in one or two sentences. Use when <the situations that should make an agent pick it>.
license: MIT
metadata:
  version: "1.0"
---
```

3. Write for the person doing the job. Say what to do and why. Name the usual mistakes. Keep it under 500 lines.
4. If it points to another skill, put the name in backticks. A test checks the name exists.

## A new check (a script inside a skill)

A check reads a file a person or agent already has and says what is wrong with it. It must not guess at facts.

1. Put it at `skills/<name>/scripts/check.py`. Plain Python, standard library only.
2. Exit 0 when clean and 1 when it found something. Print one plain line per problem, naming the item.
3. Mention the script by path in that skill's `SKILL.md`, with the file layout it expects. The validator fails if you don't.
4. Add a `good` and a `bad` example file in `examples/refund-approval/`. The good one must come out clean. The bad one must have a flaw planted for every message the script can give.
5. Add the check to `examples/run_all.sh` and raise the expected count in `tests/test_skills.py` by one.
6. Write tests: the good file is clean, each planted flaw is found by name, and one edge case where a near-miss must not be flagged.

## Before you push

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

Push only when both pass. Never chain the tests into a commit through a pipe, which hides a failure.

## Rules for wording

- Plain English. A new starter should follow it.
- No invented figures, sources or quotes. If a number is an example, say so.
- Rules of law and regulation are named, never stated as settled fact. A qualified person confirms them.

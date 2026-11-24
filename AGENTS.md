# Working in askwell

Business analyst skills for AI agents, with checkers that find vague requirements, weak stories, gaps and dead-end processes

## Run the tests

You need Python 3.10 or newer.

```bash
python scripts/validate_skills.py
python -m unittest discover -s tests
```

Every check should pass before you start and after you finish.

## Where things are

- `skills/`: the agent skills
- `tests/`: the tests
- `examples/`: worked examples
- `scripts/`: helper scripts

## Before you commit

- Make sure the checks pass.
- Put changes people will notice in `CHANGELOG.md`.
- Do not put real passwords, keys or private data in test files or examples. Use made-up ones.

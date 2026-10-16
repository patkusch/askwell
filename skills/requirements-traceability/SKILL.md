---
name: requirements-traceability
description: Builds and checks a traceability matrix that links each requirement to its objective, design and test, and finds requirements with no test or work with no requirement. Use when asked for a traceability matrix, coverage check, or proof that everything asked for was built and tested.
license: MIT
metadata:
  version: "1.0"
---

# Requirements traceability

Traceability answers two questions: "Did we build and test everything we promised?" and "Why did we build this?"

## Build the matrix

One row per requirement:

| req_id | requirement | objective | design_ref | test_ref | status |
|---|---|---|---|---|---|

- **Backward link**: every requirement points to a business objective. No link, no reason to exist.
- **Forward link**: every requirement points to a design item and at least one test.
- Keep it as a CSV or sheet so it can be checked automatically.

## Check it

```bash
python scripts/check.py matrix.csv
```

It reports requirements with no design, no test, duplicates, and anything marked done with no test. The exit code is 1 if there are gaps, so it can run in a build or a weekly check.

## Use it for

- **Coverage**: show the sponsor 100% of must-have requirements have a passing test.
- **Impact of change**: when a requirement changes, the row shows which design and tests are affected (`change-impact-assessment`).
- **Audit**: show a regulator how a rule became a feature and a test.
- **Scope creep**: work with no requirement is either a missing requirement or something to drop.

## Watch for

- A test linked to a requirement but not actually covering it. Spot-check.
- A matrix updated once and left. Update it whenever requirements, design or tests change.
- Linking to a whole document. Link to a specific item.

## Also check the tests

```bash
python scripts/check.py matrix.csv --tests tests.csv
```

`tests.csv` has one `test_id` column. This also finds tests that no requirement points at, and requirements pointing at a test that does not exist. Put several tests in one cell separated by `;`.

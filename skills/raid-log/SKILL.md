---
name: raid-log
description: Creates and maintains a RAID log of risks, assumptions, issues and dependencies with owners, ratings, mitigations and review dates. Use when asked for a risk register, issue log or assumptions list, or when a project needs a regular view of what could go wrong.
license: MIT
metadata:
  version: "1.0"
---

# RAID log

Four lists that stop surprises: **R**isks, **A**ssumptions, **I**ssues, **D**ependencies.

| Kind | What it is | Key question |
|---|---|---|
| Risk | Might happen, would hurt | What could go wrong, and how do we lower the chance or the damage? |
| Assumption | We believe it's true, haven't proved it | What are we counting on? Who will confirm and by when? |
| Issue | Already happened | Who is fixing it, by when, and what does it block? |
| Dependency | Needs something from someone else | What do we need, from whom, by when? |

## Writing a risk

Use the form: **"If [cause], then [event], leading to [effect]."**

> If the supplier file format changes without notice, the nightly import will fail, delaying orders by a day.

Rate *likelihood* and *impact* (1-5 each); score is the product. Anything 15 or above goes to the sponsor.

Choose a response: **avoid** (change the plan), **reduce** (act to lower it), **transfer** (insurance, contract), **accept** (with eyes open, and a trigger for when to act).

## Columns

| ID | Type | Description | Likelihood | Impact | Score | Owner | Response / action | Due | Status | Last reviewed |
|---|---|---|---|---|---|---|---|---|---|---|

## Rhythm

- Review weekly with the team, monthly with the sponsor.
- Every item has one named owner and a date.
- Close with a reason. Don't delete; keep history.
- An assumption that proves false becomes a risk or an issue: move it.

## Watch for

- Vague risks ("things might slip").
- No owner, or an owner who doesn't know.
- A log filled once and never read. Bring the top five to every status meeting.

## Check the log

Keep the log as a CSV with columns `id,type,description,likelihood,impact,owner,due,status,last_reviewed`, then run:

```bash
python scripts/raid.py raid.csv
```

It ranks open risks by score and flags items with no owner, no due date, overdue, not reviewed in 30 days, risks missing a rating, and any score of 15 or more that needs the sponsor. Closed items are ignored. Use `--today 2026-10-16` to check a past or future date.

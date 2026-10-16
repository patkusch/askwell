---
name: user-stories
description: Writes user stories in the "As a / I want / so that" form that are small, testable and valuable, and splits large ones. Use when asked to write or review user stories, break an epic into stories, or prepare a backlog for an agile team.
license: MIT
metadata:
  version: "1.0"
---

# User stories

A story is a promise to have a conversation. Write enough to start it, no more.

## Format

> As a **[specific role]**, I want **[a capability]**, so that **[the benefit I get]**.

The "so that" is the most important part. If you can't fill it in, the story may not be worth building.

## Check each story (INVEST)

- **I**ndependent: can be built without waiting on another.
- **N**egotiable: describes the need, not the design.
- **V**aluable: a user or the business gains something.
- **E**stimable: the team can size it.
- **S**mall: fits in one sprint, ideally a few days.
- **T**estable: you can say when it is done (see `acceptance-criteria`).

## Splitting a large story

Split by *slice of value*, not by technical layer. Try: one workflow step at a time; the simple case first, then variations; one user type at a time; one data source at a time; basic version, then performance or polish. Never split into "database", "screen", "API": nothing can be used until all three are done.

## Example

Too big: "As a customer, I want to manage my account."
Split into: change my email; reset my password; see past orders; close my account. Each has its own value and test.

## Output

```
ID / title:
As a ..., I want ..., so that ...
Acceptance criteria: (Given/When/Then)
Notes / out of scope:
Dependencies:
```

## Watch for

- "As a system..." stories. Name the person who benefits.
- Stories that are tasks ("create the table").
- Missing error cases. Ask what happens when it goes wrong.

## Check your stories

One story per line in a text file, then run:

```bash
python scripts/check.py stories.txt
```

It flags stories not in the As a / I want / so that form, roles that are too general or are "the system", a "so that" that only repeats the "I want", solution words (database, button, API), and wording that signals a story is too big or is really two.

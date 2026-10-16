---
name: acceptance-criteria
description: Writes testable acceptance criteria in Given/When/Then form that cover the normal case, edge cases and errors, so the team knows when a story is done. Use when asked for acceptance criteria, definition of done for a story, or test scenarios from a requirement.
license: MIT
metadata:
  version: "1.0"
---

# Acceptance criteria

A criterion is something a person could check and answer yes or no.

## Format

> **Given** [the starting situation], **when** [something happens], **then** [the observable result].

One behaviour per scenario. Use real values.

## Cover these cases for every story

1. **The normal path.** The thing works.
2. **Boundaries.** Smallest and largest allowed values, empty, one, many.
3. **Bad input.** Wrong format, missing field, duplicate. What message does the user see?
4. **Permissions.** Who can and cannot do it.
5. **Failure.** What if a connected system is down or the action is half done?
6. **Not-do.** Things it must *not* do, such as send an email twice.

## Example

Story: reset my password.

- Given a registered email, when I request a reset, then I get an email with a link valid for 30 minutes.
- Given an email that is not registered, when I request a reset, then the page says the same thing as for a registered one (so nobody can learn who has an account).
- Given a link older than 30 minutes, when I open it, then I'm told it has expired and can ask for a new one.
- Given a new password under 12 characters, when I submit, then I see "at least 12 characters" and the password is unchanged.

## Watch for

- Words like "quickly", "user-friendly", "easy": replace with a number or an observable fact.
- Criteria that describe the screen layout instead of the behaviour.
- Criteria that can't fail. If no case could break it, it isn't a test.

## Check your scenarios

Put scenarios in a text file, a blank line between each, then run:

```bash
python scripts/check.py scenarios.txt
```

It finds scenarios missing a Given, When or Then, steps out of order, two behaviours in one scenario, vague results ("works properly"), long chains of results, and sets that never test a failure or have fewer than three scenarios.

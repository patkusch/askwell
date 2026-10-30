---
name: requirements-writing
description: Writes and rewrites individual requirements so each one is clear, single-purpose and testable, and checks them with a bundled linter that flags vague words. Use when asked to write, tidy or review requirement statements, or when requirements read like wishes.
license: MIT
metadata:
  version: "1.0"
---

# Requirements writing

A good requirement can be read once, understood the same way by everyone, and tested.

## Shape

> **The [system / team / role] shall [do something observable] [under a condition] [to a measurable level].**

Examples:
- The system shall email the customer a receipt within 5 minutes of payment.
- The claims team shall review any claim over 10,000 within 2 working days.

## Rules

1. **One requirement per sentence.** Two "and"s usually mean two requirements.
2. **Use "shall" for must, "may" for optional.** Avoid "should": nobody knows if it's mandatory.
3. **Name the actor.** "Invoices are approved" doesn't say by whom.
4. **State the result, not the method.** Say what is needed; leave how to the designers.
5. **Give a number** for anything measured: time, size, count, percentage.
6. **No vague words**: fast, easy, user-friendly, flexible, robust, seamless, appropriate, "etc.", "and/or".
7. **Say why**, in a column beside it, so people can judge trade-offs.
8. **Give it an ID** that never changes, even if the text does.

## Use the linter

Put one requirement per line in a file, then run:

```bash
python scripts/lint.py requirements.txt
```

It flags missing "shall", "should", vague words, open-ended lists, stacked "and"s and limits with no number. Fix each, or note why it is fine. A clean run does not mean the requirement is *right*, only that it is not obviously unclear.

## Before and after

- Before: The system should be fast and easy to use.
- After: The system shall show search results within 2 seconds for 95% of searches. A new user shall complete a booking without help after a 30-minute training session.

It also flags vague quantities ("some", "several", "many", "a lot of"): say how many.

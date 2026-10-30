---
name: meeting-minutes
description: Turns meeting notes or a transcript into short minutes with decisions, actions (owner and date), open questions and risks, and prepares agendas that produce them. Use when asked to write minutes, summarise a meeting, extract action items, or plan a meeting agenda.
license: MIT
metadata:
  version: "1.0"
---

# Meeting minutes

Minutes are for people who were not there and for people who were, six weeks later. Record what was decided and who does what.

## Before: agenda

- Purpose: what must be decided or produced.
- Topics with time, owner and the outcome wanted (decide, discuss, inform).
- Pre-reads sent two days ahead.

## After: minutes (send within 24 hours)

```
Meeting / date / attendees / apologies:
Purpose:

Decisions
 1. ... (decided by ...)

Actions
 | What | Owner | Due |

Open questions
 - ... (who will find out, by when)

Risks or issues raised
 - ...

Discussion summary (only if needed)
 - Topic: two or three lines, including the reasons

Next meeting:
```

## From a transcript or messy notes

1. Find decisions: phrases like "so we'll", "agreed", "let's go with".
2. Find actions: "I'll", "can you", "by Friday". Every action needs a *name* and a *date*; if either is missing, mark it "owner needed" and ask.
3. Separate facts from opinions. Do not attribute opinions to named people unless needed.
4. Drop small talk and repetition.
5. Quote numbers and dates exactly. If unclear, mark "to confirm".

## Rules

- Actions in the minutes are chased at the next meeting, first item.
- Decisions that matter go to the decision log (`decision-log`).
- Ask attendees to reply with corrections within a day; silence is agreement.

## Pull out actions automatically

```bash
python scripts/actions.py notes.txt
```

It lists decisions and actions from raw notes and marks each action that has no owner or no date. "Someone should..." counts as no owner. Fix every flagged line before sending the minutes; the exit code is 1 while any remain.

## Check the agenda before the meeting

Hold the agenda as JSON (the layout is at the top of `scripts/agenda.py`), then run:

```bash
python scripts/agenda.py agenda.json
```

It flags no purpose or a purpose with no outcome, items that don't fit the time or leave it mostly empty, more than seven items, items with no owner or an outcome that isn't decide, discuss or inform, under 10 minutes in total set aside to decide, an agenda that is all one-way information (send an email), too much time on information, no review of last time's actions, too many people for a decision, and pre-reads sent less than two days ahead.

---
name: workshop-facilitation
description: Designs and runs a requirements or decision workshop with an agenda, timed exercises, ground rules and a record of decisions. Use when asked to plan a workshop, joint application design session, or brainstorm, or when a meeting keeps going in circles without a decision.
license: MIT
metadata:
  version: "1.0"
---

# Workshop facilitation

A workshop exists to produce something: a decision, a list, a shared picture. If you cannot name the output, do not hold it.

## Plan

1. **State the output** in one line: "By the end we will have a ranked list of the top five pain points and an owner for each."
2. **Pick the people.** Everyone who must agree to the output, and nobody who is only curious. Six to ten is the working range.
3. **Choose exercises** that fit the output:
   - Gathering ideas: silent writing on sticky notes, then group by theme.
   - Mapping a process: one person narrates, the group corrects, a scribe draws.
   - Choosing between options: dot voting, then a weighted score for the top three.
   - Surfacing risk: "imagine it is a year from now and it failed; why?"
4. **Build the agenda** with a time for each block and a 10-minute break per 90 minutes.

## Run

- Open with the output, the agenda and three ground rules: one conversation at a time, ideas before criticism, phones away.
- Write silently first, then talk. Otherwise the senior voice sets the answer.
- Keep a **parking lot** for off-topic points so they are heard but do not derail.
- Capture decisions on screen as they are made, so people can object at once.
- Close with actions: what, who, by when.

## After (same day)

Send within hours: decisions, actions with owners and dates, the parking lot, and photos of the boards.

## Output

```
Output: ...
Attendees: ...
Decisions made: 1. ... (agreed by ...)
Actions: what | who | by when
Parked: ...
```

## Check the plan

Hold the plan as JSON (the layout is at the top of `scripts/check.py`), then run:

```bash
python scripts/check.py workshop.json
```

It flags no stated output, or one you can't hold in your hand; too few or too many attendees; an agenda that doesn't fit the time or leaves too much empty; no opening or closing block; blocks with no owner, outcome or method; a block over 60 minutes or 90 minutes with no break; no silent writing step; and no parking lot.

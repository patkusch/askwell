---
name: stakeholder-communication
description: Writes status reports, executive summaries, briefings and difficult updates so busy readers see the point, the decision needed and the next step at once. Use when asked to write a project update, summarise analysis for executives, report bad news, or tailor a message to an audience.
license: MIT
metadata:
  version: "1.0"
---

# Stakeholder communication

Lead with what the reader needs. Most people read the first few lines.

## Know the reader

Before writing, answer: who is this for, what do they already know, what do they need to *do* or *decide*, how much time will they give it?

## Executive summary shape

1. **The point** in one or two sentences.
2. **The decision or action wanted**, and by when.
3. **Why**: three reasons or facts at most, with numbers.
4. **The risk or cost** of each choice.
5. **Next step.**

Put detail below, for those who want it.

## Status report

| Part | Content |
|---|---|
| Overall | Green / amber / red with one sentence of why |
| Done since last report | Results, not activity |
| Next | Planned, with dates |
| Needs a decision or help | Named person, due date |
| Risks and issues | Top three, with action |
| Numbers | Budget, date, scope: planned vs forecast |

Be honest about amber early. A red that appears with no warning breaks trust.

## Bad news

Say it first, plainly. Give the facts, the impact, what you are doing, and what you need. Don't hide it among good news; don't blame.

## Style

- Short sentences; plain words; no jargon or acronyms the reader hasn't used.
- A number with its meaning: "£40,000 a year, about two staff salaries."
- One message per paragraph.
- Give a chart only if it makes the point faster than a sentence.

## Check

Read the first three lines. Could the reader act from those alone? If not, rewrite.

## Check the summary

Save the summary or update to a text file, then run:

```bash
python scripts/check.py summary.txt
```

It flags a summary that does not say what the reader should decide in its first 60 words, one over 250 words, no figures, no cost or risk of the choice, no date, corporate jargon, long sentences, three or more hedges, and acronyms never explained. It cannot tell whether the content is right, only whether a busy reader can act on it.

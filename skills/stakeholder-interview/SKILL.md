---
name: stakeholder-interview
description: Plans and runs a one-to-one interview to draw out needs, pain points and unwritten rules, then turns the notes into confirmed findings. Use when preparing to interview a stakeholder or subject-matter expert, when given raw interview notes to structure, or when requirements feel like they are being guessed.
license: MIT
metadata:
  version: "1.0"
---

# Stakeholder interview

People describe what they do, not what they need. The job is to get from one to the other.

## Before

- Read what exists: process documents, past tickets, the org chart. Do not spend their time on what you could have read.
- Write 8-10 questions on one page, grouped by theme. Send the goal and the theme list ahead of time, not the questions.
- Book 45 minutes. Bring a second person to take notes if you can.

## Question patterns

| Aim | Ask |
|---|---|
| Understand the work | "Walk me through the last time you did this." (A real case beats a general description.) |
| Find pain | "What takes longer than it should?" "What do you redo?" |
| Find workarounds | "What do you keep in your own spreadsheet?" |
| Find the rules | "What happens when it goes wrong? Who do you call?" |
| Find the goal | "If this worked perfectly, what would be different on Monday?" |
| Test priority | "If we could only fix one thing, which?" |
| Find who else to ask | "Who else should I talk to? Who would disagree with you?" |

Ask "why" and "can you show me" more than "do you want". Avoid leading questions such as "wouldn't a dashboard help?"

## After (within 24 hours)

1. Write up the notes as **findings**, each marked *heard* (they said it), *seen* (you watched it) or *inferred* (your reading).
2. Send the findings back and ask them to correct anything wrong. This catches misunderstandings early and builds trust.
3. Pull out candidate requirements, open questions and new names to interview.

## Output

```
Interviewee / role / date:
Goal of the session:
Findings (heard / seen / inferred):
Pain points, ranked by them:
Workarounds found:
Candidate requirements:
Open questions:
Who to talk to next:
```

## Check the write-up

Write it with the headings `Interviewee`, `Date`, `Goal`, `Findings`, `Pain points`, `Workarounds`, `Candidate requirements`, `Open questions` and `Next interviews`, each finding starting `[heard]`, `[seen]` or `[inferred]`, then run:

```bash
python scripts/check.py interview.txt
```

It flags missing sections, findings with no label, more of your own reading than what was said, nothing you actually saw, pain points with no detail, candidate requirements that are really solutions, open questions with no one finding the answer, leading questions, and no sign that the findings went back to the interviewee to correct.

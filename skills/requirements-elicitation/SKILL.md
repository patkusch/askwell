---
name: requirements-elicitation
description: Chooses and combines techniques (interviews, observation, workshops, document review, prototypes, surveys) to discover what a business really needs, and records the results as a requirements list. Use when starting requirements work, when told "we don't know what we need", or when choosing how to gather requirements.
license: MIT
metadata:
  version: "1.0"
---

# Requirements elicitation

Requirements are found, not collected. Use more than one technique, because each misses something.

## Pick techniques

| Situation | Use |
|---|---|
| Few people, deep knowledge | Interviews (`stakeholder-interview`) |
| People can't say what they do | Observation: sit with them and watch |
| Many people must agree | Workshop (`workshop-facilitation`) |
| A system exists | Document and data review: forms, reports, tickets, logs |
| Users can't imagine the answer | Prototype or sketch, then react |
| Large, spread-out group | Survey, followed by interviews on surprises |
| Replacing something | Review what the old system does, then ask which parts still matter |

## Steps

1. Start from the problem statement and the stakeholder map.
2. Use two or three techniques, and compare. Where they disagree, you have found something.
3. Record every need as a numbered line: **ID, statement, source, who asked, date.** Keep the source so you can go back and ask.
4. Separate *needs* (the business outcome) from *requirements* (what the solution must do) and from *solutions* (how). Push back to the need.
5. Play it back to the stakeholders and get a written yes or a correction.
6. Mark each as: confirmed, assumed or disputed.

## Output

| ID | Need / requirement | Type (business / user / system / data) | Source | Status | Priority |
|---|---|---|---|---|---|

## Watch for

- Requirements that name a technology. Ask what it is for.
- "Everybody wants this" with no names. Find one person.
- The loudest voice winning. Check quieter users too.

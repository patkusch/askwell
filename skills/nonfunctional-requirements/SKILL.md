---
name: nonfunctional-requirements
description: Elicits and writes measurable non-functional requirements such as performance, availability, security, accessibility, privacy, auditability and usability. Use when asked about non-functional requirements, quality attributes or service levels, or when a requirements list only describes features.
license: MIT
metadata:
  version: "1.0"
---

# Non-functional requirements

Features say what the system does. These say how well. They are the usual reason a delivered system is rejected.

## Walk the checklist

For each, ask the question and push for a number.

| Area | Ask | Example of a good one |
|---|---|---|
| Performance | How fast, for how many people? | 95% of searches return in under 2 seconds with 500 users online |
| Availability | When must it be up? How long can it be down? | 99.9% from 06:00 to 22:00; recovery within 4 hours |
| Capacity | How much data now and in 3 years? | 2 million records, growing 20% a year |
| Security | Who can see or change what? | Staff see only their own region's customers |
| Privacy | What personal data? How long kept? | Delete customer data 7 years after last contact |
| Audit | What must be logged? | Every change to a price records who, when, old and new value |
| Accessibility | Which standard? | Meets WCAG 2.2 AA |
| Usability | Who are the users, how trained? | A new starter completes an order unaided after 30 minutes' training |
| Compatibility | Which browsers, devices, systems? | Current and previous version of Chrome, Edge, Safari |
| Recovery | How much data may we lose? | No more than 15 minutes |
| Support | Who looks after it? | Fixes within one business day for severity 1 |
| Legal | Which rules apply? | GDPR, sector rules |

## Rules

- Every item gets a number, a way to measure it and a condition (when, under what load).
- Say which are *must* and which are nice to have; they cost differently.
- Ask what each costs. "Always on" is very expensive; get the real need.

## Output

| ID | Area | Requirement (measurable) | How tested | Priority |
|---|---|---|---|---|

## Check your list

Keep the list as a CSV with columns `id,area,requirement,how_tested,priority`, then run:

```bash
python scripts/check.py nfr.csv
```

It flags requirements with no number or unit, a speed with no load (how many users?), availability with no percentage or hours, anything with no test or a priority that isn't must/should/could/wont, and which of the twelve checklist areas nobody has covered yet. Where an area does not apply, add a row saying so with the reason, so the gap is a decision and not an oversight.

---
name: brd-writing
description: Assembles a business requirements document with purpose, scope, stakeholders, current and future state, requirements, constraints, risks and sign-off, written for readers who must approve it. Use when asked to write a BRD, requirements specification or project requirements document.
license: MIT
metadata:
  version: "1.0"
---

# Business requirements document (BRD)

The BRD is the agreement between the business and the people building it. Write it for the person who has to sign.

## Structure

1. **Summary** (half a page): the problem, the proposed outcome, cost and time range, and the decision needed. Written last.
2. **Background and problem** (`problem-statement`).
3. **Objectives and success measures**: numbers and dates.
4. **Scope**: in, out, assumptions, constraints (`scope-definition`).
5. **Stakeholders** and their roles (`stakeholder-mapping`).
6. **Current state** in brief, with a link to the full analysis.
7. **Future state**: how the work will be done after, with a process picture.
8. **Requirements**, grouped by theme and numbered, each with a priority (`requirements-writing`, `nonfunctional-requirements`).
9. **Data and reporting needs.**
10. **Risks, dependencies and open questions** (`raid-log`).
11. **Approach and timeline**, only to the level known.
12. **Glossary.**
13. **Sign-off table**: name, role, decision, date.
14. **Version history.**

## Writing rules

- Short sentences. One idea each.
- Define each term once and use it the same way throughout.
- Prefer tables and numbered lists for requirements; prose for reasons.
- Every requirement traces to an objective. If it can't, ask why it's there.
- Mark each requirement *confirmed* or *assumed*.

## Before you send

Run `requirements-conflict-check`, and the linter in `requirements-writing`. Ask one reader who was not in the workshops to say, in their own words, what the project will deliver. Where their answer differs from yours, fix the document.

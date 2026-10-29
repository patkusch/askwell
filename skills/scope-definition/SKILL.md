---
name: scope-definition
description: Defines what a project will and will not deliver, with clear boundaries, exclusions, assumptions and a way to handle change requests. Use when writing a scope statement, when scope keeps growing, or when asked what is in or out of a project.
license: MIT
metadata:
  version: "1.0"
---

# Scope definition

Scope is a promise about what will be delivered. The *out-of-scope* list matters more than the in-scope list.

## Steps

1. **Start from the objective**: the problem statement and success measures.
2. **List deliverables** as things you can point to ("a loan approval screen", "a monthly report"), not activities.
3. **Set boundaries** on each of these:
   - Processes covered, and the ones not
   - Users, teams, regions, products
   - Systems touched and not touched
   - Data included (what history, what quality)
   - Phase: now vs later
4. **Write exclusions explicitly.** Anything a reasonable person might assume is included, but isn't, goes here. Name each one.
5. **Record assumptions and constraints** (budget, date, technology, law) and how each will be checked.
6. **Agree a change process**: who can request a change, how impact on cost, time and risk is assessed, who approves. Write it before it's needed.

## Test it

Pick five things at random from a stakeholder's wish list. For each, a stranger reading your scope should be able to say in or out. If they can't, it's vague.

## Output

```
Objective:
In scope: (deliverables)
Out of scope: (named)
Boundaries: processes / users / systems / data
Assumptions:
Constraints:
Change control: request -> impact -> decision by [name]
```

## Watch for

- "Phase 2" used as a dumping ground without a date or owner.
- Scope agreed verbally by one stakeholder. Get it signed by the sponsor.
- Small additions piling up. Keep a visible change log.

## Check the scope statement

Write it with the headings `Objective`, `In scope`, `Out of scope`, `Assumptions`, `Constraints` and `Change control`, one item per line starting with `-`, then run:

```bash
python scripts/check.py scope.txt
```

It flags missing headings, in-scope items that are activities ("investigate...") instead of things that will exist, vague wording ("etc", "as needed"), an out-of-scope list with only one item, the same thing in scope and out of scope, "phase 2" with no date or owner, and a change process that doesn't say who approves or what is assessed.

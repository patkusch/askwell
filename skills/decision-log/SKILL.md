---
name: decision-log
description: Records each significant project decision with the options considered, the reason, who decided and when, so decisions can be found and not reopened by accident. Use when asked to keep a decision log, when decisions are repeatedly re-argued, or after a meeting that made a choice.
license: MIT
metadata:
  version: "1.0"
---

# Decision log

In six months nobody remembers why. The log does.

## What to record

| Field | Content |
|---|---|
| ID and date | D-014, 2026-10-16 |
| Decision | One sentence, stated as what we will do |
| Question | The question it answers |
| Options considered | The alternatives, briefly |
| Reason | Why this one: the facts and trade-offs |
| Decided by | Name and role (the person with authority) |
| Consulted | Who gave input |
| Effect | What changes: scope, cost, date, requirements |
| Review trigger | When to revisit (date or event), if any |
| Status | Proposed, decided, superseded by D-0xx |

## Rules

- Log decisions that change scope, cost, date, design, policy or a requirement; not every small choice.
- Write it the same day, while the reason is fresh.
- Never edit an old decision. Add a new one that supersedes it and link both.
- When a decision changes requirements, update them and the traceability matrix (`requirements-traceability`).
- Share the log; a private log has no value.

## When someone reopens a decision

Show the entry. Ask: "has something changed since?" If yes, it's a new decision. If no, the log answers.

## Example

D-014. Decision: Refunds over 500 need a manager's approval. Reason: 3 of 7 audit findings last year were large refunds paid without review; a threshold limits delay to about 4% of refunds. Alternatives: all refunds approved (too slow); no approval, audit only (too risky). Decided by: Head of Finance. Review: after 3 months of data.

## Check the log

Keep it as a CSV with columns `id,date,decision,options,reason,decided_by,status,superseded_by,review_by` (options separated by `;`), then run:

```bash
python scripts/check.py decisions.csv
```

It flags decisions written as questions, fewer than two options recorded, reasons too short to explain the choice later, no named decision maker, a superseded decision that doesn't say by what (or points at one that doesn't exist or is dated earlier), proposals undecided for over 14 days, and review dates that have passed.

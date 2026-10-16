---
name: requirements-conflict-check
description: Reviews a set of requirements for contradictions, duplicates, gaps and impossible combinations, and lists the conflicts with the people who must resolve them. Use when asked to review or sanity-check requirements, when two stakeholders want opposite things, or before sign-off.
license: MIT
metadata:
  version: "1.0"
---

# Requirements conflict check

Do this before sign-off. A conflict found in a meeting costs a minute; found in testing it costs a sprint.

## Look for

1. **Direct contradictions.** "Orders are approved by the manager" against "orders over 100 are approved automatically."
2. **Duplicates** in different words. Merge them and keep one ID.
3. **Hidden conflicts.** Each is fine alone, impossible together: "keep data forever" against "delete after 7 years"; "two-second response" against "check all five systems each time."
4. **Number mismatches.** Different figures for the same limit in different places.
5. **Terminology drift.** One thing called "client", "customer" and "account". Agree a term (see `data-dictionary`).
6. **Gaps.** A process step with no one owning it, a user type with no requirements, an error case with no behaviour.
7. **Ownership conflicts.** Two teams each claim the same decision.
8. **Out-of-scope leaks.** Requirements that quietly rely on something the scope excludes.

## Method

Read through once for each type, not once for everything. Put every pair you suspect in a table. Confirm with the source before calling it a conflict.

| # | Requirements involved | What conflicts | Who decides | Options | Decision |
|---|---|---|---|---|---|

## Resolve

Don't pick a winner yourself. Bring the two owners to the same table with the options and the cost of each. Record the decision, who made it and why in the decision log (`decision-log`). Update every requirement that changed.

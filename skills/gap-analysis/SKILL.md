---
name: gap-analysis
description: Compares where the organisation is now with where it needs to be, lists the gaps and ranks them, and also covers SWOT. Use when asked for a gap analysis, SWOT, current versus target comparison, or capability assessment, or when planning what must change to reach a goal.
license: MIT
metadata:
  version: "1.0"
---

# Gap analysis (and SWOT)

## Gap analysis

1. **Define the target.** From strategy, regulation, or the problem statement. It must be specific: "answer 90% of calls within 60 seconds."
2. **Describe the current state** with the same measures (see `current-state-analysis`). Compare like with like.
3. **List the gaps** in a table, one per row, across people, process, technology, data and policy.
4. **Size each gap** as the distance in measurable terms and the effort to close it.
5. **Rank** by impact on the goal against effort, then choose what to close first.

| Area | Current | Target | Gap | Impact (H/M/L) | Effort (H/M/L) | Action | Owner |
|---|---|---|---|---|---|---|---|

## SWOT

Use SWOT when the question is strategic, not when you need a list of fixes.

- **Strengths / Weaknesses**: inside the organisation, things it controls.
- **Opportunities / Threats**: outside it, things it does not.

Make each point specific and evidenced ("two of five regions have no trained staff"). End by *acting*: pair a strength with an opportunity to exploit, and a weakness with a threat to defend against. A SWOT with no actions is decoration.

## Watch for

- A target set by feel. Ask where the number came from.
- Gaps that are really symptoms of one underlying gap. Group them.
- Listing gaps with no owner.

## Check the gap table

Keep it as a CSV with columns `area,current,target,gap,impact,effort,action,owner`, then run:

```bash
python scripts/check.py gaps.csv
```

It flags rows with no current or target, current equal to target, figures with no number, a gap that doesn't match target minus current, impact or effort not H/M/L, no action or owner, and areas (people, process, technology, data, policy) nobody looked at. It then lists the three rows to close first: highest impact for the lowest effort.

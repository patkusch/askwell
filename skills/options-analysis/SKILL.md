---
name: options-analysis
description: Frames the realistic ways to solve a problem (including doing nothing), compares them on cost, benefit, risk and feasibility, and recommends one with reasons. Use when asked to evaluate options, produce an options paper, compare build versus buy, or support a go/no-go decision.
license: MIT
metadata:
  version: "1.0"
---

# Options analysis

Decision-makers need a small set of real choices, honestly compared, and a recommendation.

## Steps

1. **State the decision** and the deadline.
2. **Generate options** widely, then cut to 3-5 that are distinct: do nothing; do the minimum (fix the process, no new technology); buy; build; a mix. Don't include an option just to make another look good.
3. **Choose criteria** that match the objectives: benefit, cost (one-off and running), time to value, risk, fit to need, effect on staff and customers, ability to change later.
4. **Describe each option** in a paragraph: what it is, what it delivers, what it doesn't.
5. **Compare** in one table, with evidence and a colour or score per cell.

| Criterion | Do nothing | Option B | Option C |
|---|---|---|---|

6. **List the risks** and key assumptions of the top two. State what would have to be true for each to be the best.
7. **Recommend** one option, say why, and say what you would do to reduce its biggest risk.
8. **Say what you don't know** and the cheapest way to find out.

## Layout of the paper

Decision needed → recommendation → options compared → reasons → risks → next steps. Put the recommendation on page one.

## Watch for

- The preferred option written with more detail than the others.
- "Do nothing" described as free. It has costs: add them.
- Quoting a cost with no range.
- Hidden constraints, such as a contract end date, that rule out an option.

## Check the options paper

Hold the paper as JSON (decision, deadline, options with costs as ranges, risks and benefit, a recommendation, unknowns), then run:

```bash
python scripts/check.py options.json
```

It flags fewer than three or more than five options, no "do nothing" option, do-nothing treated as free, costs missing or given as a single figure instead of a range, options with no risks or benefit, a recommendation for something not in the list, no biggest risk or mitigation, a recommended option described at far greater length than the rest, and no list of unknowns. The JSON layout is at the top of `scripts/check.py`.

---
name: vendor-selection
description: Compares vendors or solution options with weighted criteria, a bundled scoring script, and a structured evaluation process. Use when asked to choose a product or supplier, run an RFP evaluation, or build a decision matrix.
license: MIT
metadata:
  version: "1.0"
---

# Vendor selection

Decide the criteria and their weights *before* you see the vendors. Otherwise the weights drift toward whoever you already like.

## Steps

1. **Turn requirements into criteria.** Group into: fit to requirements, cost over the full life, risk (vendor stability, exit options), support, security and compliance, integration, user experience.
2. **Mark knock-outs**: must-haves that disqualify a vendor if missing (data residency, certification). Apply these first.
3. **Weight** the criteria so weights add up to 100. Get the sponsor to agree them in writing.
4. **Collect evidence**: written answers, demos running *your* scenarios, reference calls, a trial. Don't score from the sales deck.
5. **Score 1-5** with a written reason per score. Have at least two people score independently, then reconcile differences.
6. **Calculate**:

```bash
python scripts/score.py scorecard.json
```
```json
{"criteria": {"Fit": 40, "Cost": 30, "Support": 30},
 "scores": {"Vendor A": {"Fit": 4, "Cost": 3, "Support": 5},
            "Vendor B": {"Fit": 5, "Cost": 2, "Support": 3}}}
```
The script checks weights add up to 100 and scores are in range.

7. **Check robustness.** Move weights by ±10 points. If the winner changes, the choice is close; say so and decide on the factor that matters most.
8. **Recommend** with the top two options, the main trade-off between them, and total cost of ownership.

## Watch for

- Cost scored on licence only. Include implementation, training, support and exit.
- Demos staged by the vendor. Give them your scenarios in advance, but not your scoring.
- Conflicts of interest; record any.

## Is the winner safe?

The script also moves ten points of weight onto, and then off, each criterion in turn and reports every case where a different vendor would win. If the winner changes under small shifts, the vendors are close on what you said mattered, so decide on the factor you care about most. It also prints the lead over second place.

## Knock-outs

Add `"knockouts": {"Vendor A": ["no EU data residency"]}` to the JSON to take a vendor out before scoring because it fails a must-have. Excluded vendors are listed with the reason and are not ranked. If every vendor is knocked out the script stops and says so, because that means the must-have or the search needs to change.

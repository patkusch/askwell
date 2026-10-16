---
name: business-case
description: Builds a business case with costs, benefits, payback, net present value, ROI and sensitivity checks, using a bundled calculator. Use when asked for a business case, cost-benefit analysis, ROI or payback calculation, or to justify an investment.
license: MIT
metadata:
  version: "1.0"
---

# Business case

Show decision-makers what it costs, what they get, when, and how sure you are.

## Steps

1. **Define the options**, always including **do nothing**, with its own cost (the problem keeps costing money).
2. **List costs**: one-off (build, buy, train, migrate) and running (licences, support, staff time). Include internal staff time and ongoing change.
3. **List benefits** in money where honest: time saved × cost per hour *only if the time is actually freed up*; errors avoided × cost per error; revenue; risk reduced. Keep non-money benefits as a separate list (customer satisfaction, compliance).
4. **Set a period** (usually 3-5 years) and a discount rate (ask finance).
5. **Run the numbers**:

```bash
python scripts/case.py case.json
```

Input:
```json
{"discount_rate": 0.08, "upfront_cost": 100000,
 "yearly_benefits": [40000, 50000, 50000], "yearly_costs": [5000, 5000, 5000]}
```
It returns net present value, payback in years, ROI and IRR.

6. **Test the sensitivity.** Rerun with benefits 30% lower and costs 30% higher. If the case collapses, say so and what must hold true.
7. **State assumptions**, who gave each number, and how confident you are.

## What the numbers mean

- **NPV**: the value today of all future gains minus costs. Above zero means it earns more than the discount rate.
- **Payback**: how long until you have your money back.
- **ROI**: net gain divided by total cost, as a percentage.

## Watch for

- Benefits counted twice, or "saved time" that no one will bank.
- Costs left out: support, training, data clean-up, the people who must stay on the old system.
- A single number presented as certain. Give a range.

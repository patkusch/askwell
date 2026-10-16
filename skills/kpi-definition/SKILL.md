---
name: kpi-definition
description: Defines KPIs and success measures that link to a business goal, with an exact formula, data source, owner, target and review rhythm. Use when asked to define metrics, set success criteria, build a measurement plan, or when a report's numbers are disputed.
license: MIT
metadata:
  version: "1.0"
---

# KPI definition

A metric nobody can act on is decoration. Each one should change a decision.

## Steps

1. **Start from the goal**, not the data. "Reduce late deliveries" before "on-time %".
2. **Pick few.** One main measure per goal, plus one or two that guard against harm (if you push speed, also watch quality).
3. **Mix leading and lagging.** Lagging shows the result (churn); leading shows early signs you can still act on (support tickets per user).
4. **Define each one completely:**

| Item | Example |
|---|---|
| Name | On-time delivery rate |
| Purpose | Are customers getting orders when promised? |
| Formula | Orders delivered on or before promised date ÷ orders delivered, in the month |
| Includes / excludes | Excludes orders held at the customer's request |
| Data source | Orders table, `promised_date`, `delivered_date` |
| Frequency | Monthly, with weekly view |
| Baseline | 82% (Jan-Mar 2026) |
| Target | 95% by Dec 2026 |
| Owner | Head of Logistics |
| Action if off target | Review at the monthly ops meeting; root cause on any region below 90% |

5. **Check it can be gamed.** If staff are rewarded on it, what shortcut raises the number without helping? Add a guard.
6. **Confirm the data exists** and who fixes it when it's wrong (`data-dictionary`).
7. **Fix the baseline** before the project starts, or you cannot show improvement.

## Watch for

- Averages hiding a spread; show a percentile for time-based measures.
- Percentages without counts: 100% of 3 is not 100% of 3,000.
- Too many measures. If everything is a KPI, nothing is.

## Check your KPIs

Write each KPI as a JSON object with `name, purpose, formula, source, owner, frequency, baseline, target, guard, action`, then run:

```bash
python scripts/check.py kpis.json
```

It flags anything missing, a target or baseline with no number, a formula that does not say what is counted, duplicate names, and a list of more than eight.

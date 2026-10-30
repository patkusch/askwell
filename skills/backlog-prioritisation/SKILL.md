---
name: backlog-prioritisation
description: Ranks requirements or backlog items using MoSCoW, RICE or WSJF and a bundled scoring script, and explains the trade-offs to stakeholders. Use when asked to prioritise a backlog, choose what goes in a release, or settle a dispute about what comes first.
license: MIT
metadata:
  version: "1.0"
---

# Backlog prioritisation

Prioritising is choosing what not to do yet. Pick a method, apply it openly, and keep the reasons.

## Choose a method

| Method | Use when | How |
|---|---|---|
| **MoSCoW** | Fixed date or budget; agreeing a release | Must / Should / Could / Won't *this time*. Musts alone should be deliverable; cap Musts at about 60% of effort |
| **RICE** | Product features with usage data | Reach × Impact × Confidence ÷ Effort |
| **WSJF** | Mixed work with deadlines and risk | (Business value + Time criticality + Risk reduction) ÷ Job size |
| **Value vs effort** | Quick workshop | Plot on a 2×2; do high value, low effort first |

## Run the scoring

```bash
python scripts/score.py rice items.csv
python scripts/score.py wsjf items.csv
```

RICE columns: `id,name,reach,impact,confidence,effort` (confidence 0 to 1). WSJF columns: `id,name,business_value,time_criticality,risk_reduction,job_size`. Score values on a shared relative scale (for example 1, 2, 3, 5, 8, 13), with the group agreeing each one.

## Steps

1. Agree the **goal** the ranking serves this quarter.
2. Score as a group; the people who do the work give effort, the business gives value.
3. Run the script, then **sanity-check**: does the top five feel right? If not, find out what the model is missing, rather than overriding quietly.
4. Check **dependencies**: an item that unlocks others moves up.
5. Publish the ranking *with* the scores and the "won't do now" list.

## Watch for

- Everything is "high". Force a ranking: only a few can be first.
- Scores that are really opinions of the loudest person. Ask for evidence.
- Effort left out. A big win that takes a year may lose to three small ones.
- Legal and safety items: treat as must-do, outside the scoring.

## Check a MoSCoW split

```bash
python scripts/score.py moscow items.csv
```

Columns: `id,name,moscow,effort`. It shows the share of planned effort in Must, Should and Could, and warns when Musts take more than 60%, which leaves no room for surprises.

For RICE and WSJF, `--top 5` shows only the first five. Neighbours whose scores are within 10% are reported as ties: the scores are guesses, so a 4% gap is not a reason to put one first. Choose between them on dependencies and risk.

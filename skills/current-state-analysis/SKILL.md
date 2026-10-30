---
name: current-state-analysis
description: Documents how a process, system or team works today, including volumes, delays, handoffs and workarounds, so a future state can be compared against it. Use when asked for an as-is analysis, baseline, or process assessment, or before proposing any change.
license: MIT
metadata:
  version: "1.0"
---

# Current-state analysis

You cannot show an improvement without a baseline. Capture how it really works, not how the manual says.

## Steps

1. **Define the boundary.** Where does the process start and end? What triggers it?
2. **Observe, don't only ask.** Watch two or three real cases end to end. Compare with the written procedure and note every difference.
3. **Map it** (see the `process-mapping` skill): steps, who does each, systems used, handoffs.
4. **Measure it.** For each step: volume, time spent, time waiting, error or rework rate. Pull system data where possible and treat anecdotes as leads.
5. **Log the pain.** Delays, rework, manual copying, approvals that add nothing, workarounds, risks, compliance gaps.
6. **Summarise** what is working (keep it), what is not (fix it), and what is unknown.

## Output

```
Scope and trigger:
Process map: (link or diagram)
Volumes: per day/week/month
Time: touch time vs waiting time, end to end
Quality: error / rework rate
Systems and data used:
Pain points: ranked, with evidence
Workarounds found:
Strengths to keep:
Unknowns to resolve:
```

## Watch for

- The "tribal" steps nobody wrote down. Ask "what do you do when the system won't let you?"
- Averages that hide a long tail. Show the median and the worst 10%.
- Measuring only the happy path. Include exceptions: they often cost the most.

## Check the table and see where the time goes

Keep the steps as a CSV with columns `step,role,system,kind,volume_per_week,touch_minutes,wait_minutes,error_rate_pct,evidence`, then run:

```bash
python scripts/check.py current_state.csv
```

It flags steps with no role or system, missing or negative numbers, an error rate over 100%, evidence that isn't measured, observed or estimated, long waits that are only guesses, a table with no exception steps (happy path only), and a table that is mostly estimates. It then prints how much of the end-to-end time is work and how much is waiting, the longest wait, and the step that makes the most errors a week.

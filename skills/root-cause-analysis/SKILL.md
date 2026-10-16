---
name: root-cause-analysis
description: Finds the real cause of a recurring problem using five whys, cause-and-effect diagrams and evidence checks, and separates causes from symptoms. Use when a problem keeps coming back, when asked for a root cause, 5 whys or fishbone analysis, or after an incident or failed delivery.
license: MIT
metadata:
  version: "1.0"
---

# Root cause analysis

Fixing a symptom leaves the problem to return. Keep asking why until the answer is something you can change.

## Method

1. **State the problem** with a number and a date: "42 invoices were wrong in March."
2. **Brainstorm causes** by category (fishbone): people, process, systems, data, policy, environment, suppliers. Write many; judge later.
3. **Five whys** on the most likely branches. Each "because" must be a fact you can check, not a guess. Stop when the answer is something the organisation controls and can fix.
4. **Test with evidence.** For each candidate cause, find data that would prove or disprove it. Count how many cases it explains.
5. **Rank** causes by how many cases they explain (a Pareto view usually shows two or three causes drive most of the trouble).
6. **Choose fixes** that remove the cause, not just catch the effect. Say how you will know it worked.

## Example

Problem: orders ship late.
Why? Picks start late. Why? Pick lists print at 10:00. Why? The overnight import fails and is rerun by hand. Why? The supplier sends files with a changed column order. Why? Nobody agreed a file format with them. **Root cause:** no agreed supplier file format. **Fix:** agree and validate the format; do not just rerun the import faster.

## Output

```
Problem (with numbers):
Candidate causes (by category):
Why-chain for top causes:
Evidence for / against each:
Root cause(s):
Fix and owner:
How we will know it worked:
```

## Watch for

- Blaming a person. If the answer is "someone made a mistake", ask why the process allowed it.
- Stopping at the first plausible answer.
- More than one root cause: this is normal.

---
name: stakeholder-mapping
description: Identifies everyone affected by or able to influence a project, rates their power and interest, and plans how to engage each one. Use when starting a project, when a project is stalling because of people nobody consulted, or when asked for a stakeholder register, power/interest grid or RACI.
license: MIT
metadata:
  version: "1.0"
---

# Stakeholder mapping

Find the people who can make the project succeed or fail, then decide how to work with each.

## Steps

1. **List candidates.** Walk through these groups so nobody is missed: sponsor, budget holder, process owners, the people who do the work today, customers or end users, IT and security, legal and compliance, finance, suppliers, and anyone whose job changes if this succeeds.
2. **Rate each one** on two scales, high or low: *power* (can they stop or approve it?) and *interest* (does it change their day?).
3. **Place them on the grid** and pick an approach:
   - High power, high interest: *manage closely.* Regular one-to-ones.
   - High power, low interest: *keep satisfied.* Short updates, no surprises.
   - Low power, high interest: *keep informed.* Newsletters, demos, a channel to ask questions.
   - Low power, low interest: *monitor.*
4. **Record their stance** (supporter, neutral, resistant) and *why*. Resistance usually has a reason worth hearing: lost work, lost status, extra effort.
5. **Assign a RACI** for the key deliverables: one Accountable per item, no more.

## Output: stakeholder register

| Name / role | What they care about | Power | Interest | Stance | How we engage | Owner |
|---|---|---|---|---|---|---|

## Watch for

- The person who does the work every day but is not on the org chart as a decision-maker. Ask the sponsor: "who will be upset if we get this wrong?"
- Two people who both think they own the same thing. Name one owner.
- Registers go stale. Review at each phase gate.

## Check the register

Keep it as a CSV with columns `name,role,cares_about,power,interest,stance,engagement,owner`, then run:

```bash
python scripts/check.py register.csv
```

It flags missing ratings, a stance that is not supporter, neutral or resistant, no engagement plan, no owner for the relationship, a resistant person whose reason isn't written down, a high-power resistant stakeholder who isn't managed closely (your biggest risk), a high-power high-interest person not managed closely, and groups nobody is listed for (sponsor, the people who do the work, customers, technology, risk or compliance, finance).

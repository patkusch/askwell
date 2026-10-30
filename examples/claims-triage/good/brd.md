# Business requirements: claims triage

## Summary
Motor claims are worked in the order they are reported, so injured customers wait a median of 19 hours for a first call and generate about 30 complaints a month. We propose triage bands set by rules from the first notice of loss, with urgent claims at the top of every handler's list. It costs 70,000 to 110,000 to set up. We need the sponsor's decision by 20 November so it is live before the winter weather peak.

## Problem and background
The claims system has no urgency field. Handlers sort by hand each morning.

## Objectives
- Median first contact for urgent claims under 4 hours by March 2027.
- Complaints about slow contact below 10 a month.

## Scope
In scope: triage bands, rule table, claim received text.
Out of scope: home and travel claims, policy platform changes, fraud scoring.

## Stakeholders
| Name | Role | Interest |
|---|---|---|
| Helen Marsh | Sponsor | Faster contact, fewer complaints |

## Requirements
| ID | Requirement | Priority |
|---|---|---|
| BR-001 | The system shall assign every new motor claim a triage band within 2 minutes of first notice of loss | Must |
| BR-002 | The claims handler shall contact the customer within 4 working hours of a claim in the urgent band | Must |
| BR-003 | The system shall log each triage band change with the person, the time, the old band and the new band | Must |

## Risks, assumptions and dependencies
The vendor release carrying the rule table may slip; the date will be agreed in writing.

## Sign-off
| Name | Role | Decision | Date |
|---|---|---|---|
| Helen Marsh | Sponsor | | |

## Version history
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-30 | First issue |

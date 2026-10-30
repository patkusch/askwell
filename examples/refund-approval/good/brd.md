# Business requirements: refund approval

## Summary
Refund agents retype amounts between two screens, which led to about 40 wrongly paid refunds a month and a median wait of 71 hours for a decision. We propose a single approval step that passes the approved amount straight to payment and tells the customer within minutes. It costs 40,000 to 70,000 to set up. We need the sponsor's decision by 15 November so the work is live before the December month-end.

## Problem and background
Two billing screens share no data. Agents copy amounts by hand and managers approve large refunds by email.

## Objectives
- Wrongly paid refunds below 5 a month by December 2026.
- Median decision time under 24 hours.

## Scope
In scope: waiting list, approval screen, decision email.
Out of scope: refunds under 500, billing system changes, chargebacks.

## Stakeholders
| Name | Role | Interest |
|---|---|---|
| Priya Nair | Sponsor | Fewer audit findings |

## Requirements
| ID | Requirement | Priority |
|---|---|---|
| BR-001 | The system shall email the customer a decision within 5 minutes of approval | Must |
| BR-002 | The finance manager shall approve any refund over 500 within 2 working days | Must |
| BR-003 | The system shall record who approved each refund, when, and the amount | Must |

## Risks, assumptions and dependencies
Integration with billing may take longer than planned; a two-week trial will test it.

## Sign-off
| Name | Role | Decision | Date |
|---|---|---|---|
| Priya Nair | Sponsor | | |

## Version history
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-16 | First issue |

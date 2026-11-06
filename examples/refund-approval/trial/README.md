# A live trial of the review method

On 6 November 2026 two AI agents ran `requirements-review` on the eight refund requirements in this folder. The first agent hunted for problems. The second got only the claims and the requirements, not the first agent's reasoning, and tried to disprove each claim.

These are the records they wrote. Two things were changed afterwards: the second agent's reasoning was moved into the `why_it_stands` line, which the skill did not have yet, and the line endings were tidied.

```bash
python3 skills/requirements-review/scripts/check.py examples/refund-approval/trial/review_findings.json examples/refund-approval/trial/review_requirements.csv examples/refund-approval/trial/review_coverage.csv --report
```

## What happened

- The first agent raised 10 candidates.
- The second confirmed 7, left 1 waiting for an answer, and rejected 2.
- Both rejected candidates were the same problem as another candidate, filed under a different pass. None was rejected for being wrong.
- The agents found all four problems in the hand-written example: two approvers for one refund, delete against keep, nobody to approve a refund from 50 to 400, and customer against client.
- They found four more that the hand-written example did not have: nobody is named to reject a refund, nothing says how the system knows a refund was paid, nothing says what happens when an approver misses the deadline, and a customer may have only an email address or only a mobile number.
- Neither agent had a list of stakeholders, so each "who decides" names the role that is needed and no person.

## What the trial changed

The two agents listed 24 places where the skill was unclear or made them guess. The fixes that followed:

- The eight passes say how a contradiction, a hidden conflict and two owners differ. The hand-written example had filed "two approvers" under the wrong one.
- A rule for confirmed against needs-answer.
- The second reviewer's brief has a test for gaps and for two owners, not only for conflicts.
- A coverage cell can say `see F1`, and a rival reading is rejected with `same_as`.
- The second reviewer writes down why a finding stands.
- A yardstick for high, medium and low.

## What it does not show

- It is one run on eight requirements.
- Both agents were the same AI model, so they may share blind spots. A second reviewer of a different kind, or a person, is a stronger check.
- No candidate was plainly wrong, so the trial does not show the second reviewer catching a false alarm.
- No business analyst has judged whether the seven confirmed findings are right.

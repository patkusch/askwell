---
name: user-acceptance-testing
description: Plans and runs user acceptance testing where business users confirm a solution works for real work, with scenarios, entry and exit criteria, defect handling and sign-off. Use when asked to plan UAT, write UAT scripts, triage defects found by users, or prepare for go-live sign-off.
license: MIT
metadata:
  version: "1.0"
---

# User acceptance testing (UAT)

UAT asks one question: can the business do its work with this? It is not for finding every bug; that is earlier testing.

## Plan

1. **Entry criteria**: system and integration testing finished; no open critical defects; test data and accounts ready; testers trained and released from other work.
2. **Pick testers** who do the job daily, plus a few who are awkward.
3. **Write scenarios from real work**, mapped to requirements and acceptance criteria (`acceptance-criteria`). For each:

| ID | Requirement | Scenario | Steps | Test data | Expected result | Result | Defect ID |
|---|---|---|---|---|---|---|---|

4. **Cover** end-to-end flows, month-end or peak cases, reports, roles and permissions, and error handling, not only the happy path.
5. **Schedule** with time to fix and retest, usually twice what you first think.

## Run

- Brief testers: what to test, how to log, how to tell a defect from a change request.
- A **defect** is "it does not do what was agreed." A **change request** is "I now want something different." Log both, handle separately.
- Triage daily. Severity: *critical* (blocks work, no workaround), *major* (workaround exists), *minor* (cosmetic).
- Retest every fix. Rerun nearby scenarios for regression.

## Exit and sign-off

Agree beforehand. For example: all must-have scenarios passed; no open critical or major defects; remaining minor ones accepted with an owner and date; business owner signs.

Output a one-page result: scenarios run, passed, failed, defects by severity, risks accepted, and a clear recommendation: go, go with conditions, or no-go.

## Watch for

- Testers too busy to test. Get time agreed in advance.
- Using fake data too neat to find real problems.
- Sign-off by someone who didn't test.

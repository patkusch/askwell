# Changelog

## Unreleased
- `requirements-review`: a full review where every finding quotes the requirement word for word, a second reviewer tries to disprove it, and a coverage sheet shows what was looked at. Its check finds quotes that are not in the requirement, findings nobody double-checked, ratings on unconfirmed findings, placeholder names, and requirements nobody reviewed. `--start` writes an empty coverage sheet, `--brief` prints what the second reviewer may see, `--previous` holds a new review to what the last one settled, `--report` writes the report from the records, and `--json` is for other tools.
- The review method was tried live by two agents on the refund example. Their records are in `examples/refund-approval/trial`, with a note on what the trial changed and what it does not show.
- `askwell.py audit --json`, `askwell.py new` and `askwell.py files`, with a generated guide to which file name each check reads.
- Business case compares several options side by side. Vendor scorecard knocks out vendors that fail a must-have. Backlog shows only the top N and reports scores too close to call. Acceptance criteria catch a scenario that repeats an earlier one.
- Issue templates, a security policy, Dependabot and a citation file.

Work before this log (33 skills, 35 checks, the refund-approval and claims-triage examples, the router and the domain packs) is in the commit history.

---
name: requirements-review
description: Runs a full review of a set of requirements where every finding quotes the requirement word for word, is checked by a second reviewer who tries to disprove it, and is recorded as confirmed, waiting for an answer or rejected, with a sheet that shows what was looked at. Use when asked for a thorough or independent review of requirements, before sign-off on a large or costly set, when an earlier review raised false alarms, or when several agents or people share one review.
license: MIT
metadata:
  version: "1.0"
---

# Requirements review

A review is worth only as much as its findings can be trusted. Reviews fail in two ways. They raise false alarms, because the reviewer misread a requirement and nobody looked again. And they stay silent about gaps, because "nothing found" looks the same whether somebody looked or not.

This method closes both with three rules:

1. **Quote, never retell.** Every finding carries the exact words of each requirement it is about.
2. **The finder never checks their own finding.** A second reviewer gets each one and tries to disprove it.
3. **Write down what was looked at.** Every requirement, every pass, so a clean result means "looked and found nothing".

For a quick look by one reviewer, use `requirements-conflict-check`. Use this skill when a wrong finding or a missed one would cost real money or time.

## Steps

1. **List what is under review.** Put the requirements in `review_requirements.csv` with the columns `id,text`, one requirement per row. Fix the wording first with `requirements-writing`, so the review is about what the requirements say and not how they are written. If the wording is not yours to change, list the unclear words on the side. This review does not rate wording.

2. **Make the coverage sheet.** `review_coverage.csv` has one row per requirement and one column per pass. There are eight passes:

   | Pass | What it looks for |
   |---|---|
   | contradiction | In the same case, one requirement says to do what another forbids or does differently |
   | duplicate | The same requirement written twice in different words |
   | hidden-conflict | No clash in the words, but a case comes up where meeting one breaks the other, often with time or volume |
   | number-mismatch | Different figures for the same limit |
   | term-drift | One thing under several names |
   | gap | A case, a user, a step or a decision that nothing covers, such as a decision nobody is given |
   | ownership | Two people or teams given the same decision, where both could act and nothing says whose word counts |
   | scope-leak | A requirement that relies on something the scope leaves out |

   Start the sheet with every cell empty, so nothing counts as looked at until you fill it in. The first column is called `requirement`:

   ```bash
   python scripts/check.py --start review_requirements.csv > review_coverage.csv
   ```

   To tell the first three apart: if both can be met by two people each doing their part, it is ownership. If the words clash in a case both requirements cover, it is a contradiction. If they clash only once something else happens, such as an account staying open for eight years, it is a hidden conflict.

3. **Hunt, one pass at a time.** Read the whole set once for each pass, not once for everything. Each suspicion is a candidate, not yet a finding. As you finish a pass, fill in its column: `clear`, the finding id, or `skipped: why`. Never leave a cell empty and never write `clear` for a pass you did not do.

   One problem often turns up in more than one pass. Record it once, under the pass that fits best. In the other cells where you met it, write `see F1`, so the sheet does not say `clear` about something you found.

   - **How low is the bar?** Raise a candidate when you can say what would go wrong. Leave out a "what if" that no requirement touches.
   - **What does a gap quote?** A gap is something no requirement says, so name the requirements at its edges and quote those edges. A refund from 50 to 400 with no approver names the rule that stops at 50 and the rule that starts at 400.
   - **What does `clear` mean for a gap?** That you found no gap touching that requirement.
   - **No scope statement?** Write `skipped: no scope statement` in the scope-leak column. Do not guess the scope from the requirements.
   - **Several findings in one cell?** Separate the ids with a space.
   - **Want leads?** If you have it, `conflicts.py` in `requirements-conflict-check` points at likely duplicates, number mismatches, "must" against "must not", and drifting names. It is a help, not a step. Every pass can be done by reading.

   A candidate is a finding with only `id`, `kind`, `requirements`, `quotes`, `what` and `found_by` filled in. Keep your reasoning in a `notes` line of the record. A candidate keeps its id for good, even if it ends up rejected.

4. **Hand every candidate to a second reviewer.** For agents, start a fresh agent and give it only the candidate and the requirements, not the finder's reasoning. A reviewer who is shown the argument tends to agree with it. For people, ask a colleague who did not write the finding. Give them this brief:

   ```
   You did not write this finding. Try to disprove it.
   Read each requirement it names in full, not only the quoted words.
   For a conflict: is there a reading in which both requirements can be met?
   For a gap: is the case really uncovered, or does another requirement cover it?
   For two owners: does anything say whose word counts?
   Is something missing that only a named person can tell us?
   Answer with one verdict: confirmed, needs-answer or rejected, and say why.
   ```

   The script prints this brief with the claim and each requirement in full, and leaves out the finder's notes, name and verdict:

   ```bash
   python scripts/check.py --brief review_findings.json review_requirements.csv F3
   ```

   Leave off the id to print every finding.

   The second reviewer may correct a candidate that is right in substance: its pass, its wording, its quotes, or the requirements it names. The id stays. They also get any scope statement or glossary the project has, because a gap or a drifting name cannot be tested without them.

5. **Record one of three verdicts.**

   | Verdict | Means | Must have |
   |---|---|---|
   | confirmed | The second reviewer could not disprove it | What the second reviewer tried and why it stands, what goes wrong if it is left, how bad (high, medium or low), who decides |
   | needs-answer | It turns on one fact the documents do not give | Why it could not be settled, the exact question, and who can answer it. No rating yet |
   | rejected | The second reviewer disproved it | The reason. Keep the record so the next review does not raise it again |

   How bad is it? Rate by what happens if nobody fixes it:

   | Rating | What happens |
   |---|---|
   | high | The thing cannot be built as written, or people lose money, break a rule, or are treated wrongly |
   | medium | It gets built, then has to be reworked, or staff need a workaround |
   | low | It confuses a reader but the build comes out the same |

   Two candidates that turn out to be one problem: keep the one under the pass that fits best. Reject the other with `same_as` set to the id of the one you kept, so the record shows it was merged and not disproved.

   Confirmed or needs-answer? If the problem is real whichever way the missing fact goes, it is confirmed. If the fact decides whether there is a problem at all, it is needs-answer. A missing decision ("who approves a refund from 50 to 400?") is a confirmed gap: the requirements have to say it either way. A missing fact ("does every customer have a mobile number?") is needs-answer.

   When the answer comes, the finding goes back to a second reviewer with the answer, and ends as confirmed or rejected. Do not settle it yourself because you asked the question.

6. **Run the check.**

   ```bash
   python scripts/check.py review_findings.json review_requirements.csv review_coverage.csv
   ```

   It prints one line per problem and exits 1 if there is any. Fix the records and run it again.

7. **Write the report from the records.** Add `--report` and the script prints the report: confirmed findings worst first, questions to answer, what was rejected and why, and what was not looked at. It prints only when the records pass, so the report cannot say something the records do not.

## The findings file

`review_findings.json` is a list. One finding looks like this:

```json
{
  "id": "F1",
  "kind": "ownership",
  "verdict": "confirmed",
  "requirements": ["R2", "R5"],
  "quotes": {
    "R2": "any refund over 500",
    "R5": "any refund over 400"
  },
  "what": "A refund over 500 has two approvers with two deadlines.",
  "found_by": "reviewer-1",
  "checked_by": "reviewer-2",
  "why_it_stands": "Looked for a rule that says whose approval counts. There is none.",
  "impact": "Nobody knows whose approval counts, so large refunds wait.",
  "severity": "high",
  "who_decides": "Head of Finance"
}
```

A needs-answer finding has `open_question` and `who_can_answer` in place of the last three lines, and keeps `why_it_stands`. A rejected finding has `reason`.

## Reviewing the same requirements again

Keep the findings file from the last review as `review_previous.json` and pass it in:

```bash
python scripts/check.py review_findings.json review_requirements.csv review_coverage.csv --previous review_previous.json
```

The check then holds the new review to what the old one settled:

- A finding that was rejected stays on record as rejected, so nobody spends the same hour on it again.
- A rejected finding may come back under another verdict only with a `what_changed` line that says what is different now.
- A question that was waiting for an answer may not vanish. Answer it, or carry it over.

A finding about a requirement that no longer exists is dropped without complaint.

## What the check finds

- A quote that is not in the requirement word for word, a requirement with no quote, or a quote of one word (one word is enough only to show a name, in the term-drift pass).
- A finding with no second reviewer, or found and checked by the same one, or with no word from the second reviewer on why it stands.
- A confirmed finding that does not say what goes wrong, how bad, or who decides.
- "TBD", "unknown" or the like where a person or a role should be.
- A rating on a finding that is not confirmed.
- A needs-answer finding with no question or nobody to ask, and a rejected one with no reason.
- One finding recorded twice.
- With an earlier review passed in: a rejected finding that is missing or back with no reason, and an open question that vanished.
- A requirement listed twice, or with no text.
- A requirement that is not in the coverage sheet, an empty cell, or a skip with no reason.
- A finding the coverage sheet does not show, and a sheet that names a finding that does not exist.

## What it cannot tell you

- It proves the quoted words are there. It does not prove they mean what the finding says.
- It proves two names are on each finding. It does not prove the second reviewer worked alone.
- It proves every cell is filled. It does not prove the pass was done well.

## Watch for

- **Rating before confirming.** A rating on a hunch makes it look settled. Confirm first.
- **Needs-answer as a parking place.** It is for one exact missing fact and a named person who knows it. A vague worry is a candidate to reject or to work on.
- **No list of stakeholders.** Write the role the decision needs, such as "whoever owns the refund approval rules". Do not make up a name or a job title, and do not write TBD: the check reports it. `stakeholder-mapping` gets you the list.
- **Throwing away rejected findings.** Without the record, the next reviewer raises the same thing and the same hour is spent again.
- **Picking a winner.** The review says what conflicts and who decides. The owners decide, and the decision goes in the log (`decision-log`).
- **Requirements that change after the review.** Run the check again. Quotes that no longer match show which findings need a fresh look.

## Where the method comes from

Security code audits work this way: a ledger of what was covered, a fresh reviewer who tries to disprove each finding, and three verdicts. Cloudflare's [security-audit skill](https://github.com/cloudflare/security-audit-skill) is a public example. This skill applies the same idea to requirements.

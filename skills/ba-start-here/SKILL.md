---
name: ba-start-here
description: Routes any business analysis request to the right skills in the right order, and asks the one question that matters when the request is unclear. Use when a request involves requirements, process change, a business case, a project start, or "help me as a business analyst", or when unsure which BA skill applies.
license: MIT
metadata:
  version: "1.0"
---

# Start here: which skill, in what order

## 1. Work out where the work stands

| What the person says | Stage | Start with |
|---|---|---|
| "We need a system / dashboard / app for X" | Unclear problem | `problem-statement` |
| "Something keeps going wrong" | Diagnosis | `root-cause-analysis`, `current-state-analysis` |
| "Who do I need to talk to?" | Starting | `stakeholder-mapping`, then `stakeholder-interview` |
| "What should we build?" | Requirements | `requirements-elicitation` |
| "Write the requirements / BRD" | Documenting | `requirements-writing`, `brd-writing` |
| "Write user stories" | Agile delivery | `user-stories`, then `acceptance-criteria` |
| "Is it worth doing?" | Justifying | `options-analysis`, `business-case` |
| "Which supplier or product?" | Choosing | `vendor-selection` |
| "What goes first?" | Planning | `backlog-prioritisation` |
| "Draw how it works" | Modelling | `process-mapping` |
| "Review these requirements" | Quality check | `requirements-conflict-check`, `requirements-writing` |
| "Are we ready to go live?" | Delivery | `user-acceptance-testing`, `change-impact-assessment` |
| "Write the update / minutes" | Reporting | `stakeholder-communication`, `meeting-minutes` |
| Regulated or specialist field | Context | `domain-packs` as well |

## 2. The usual order for a whole project

1. **Understand**: `problem-statement` → `stakeholder-mapping` → `current-state-analysis`
2. **Find the need**: `stakeholder-interview`, `workshop-facilitation`, `requirements-elicitation`, `root-cause-analysis`
3. **Define**: `scope-definition` → `requirements-writing` → `user-stories` / `use-cases` → `acceptance-criteria` → `nonfunctional-requirements` → `data-dictionary`
4. **Check**: `requirements-conflict-check` → `requirements-traceability`
5. **Justify and choose**: `options-analysis` → `business-case` → `vendor-selection` → `backlog-prioritisation`
6. **Deliver**: `user-acceptance-testing` → `change-impact-assessment` → `kpi-definition`
7. **Throughout**: `raid-log`, `decision-log`, `meeting-minutes`, `stakeholder-communication`

## 3. Ask one question if you must

If you can't tell what is wanted, ask exactly one:

> What is the decision or deliverable this has to support, and who will read it?

Don't ask a list. State your assumption and carry on if the answer is likely.

## 4. Operating rules for every BA task

1. **Problem before solution.** If the request names a tool, find the need behind it.
2. **Keep facts, assumptions and opinions apart.** Label each one.
3. **Every number needs a source.** If you don't have one, say "not known" and say how to find out. Never invent figures, names, dates or quotes.
4. **Every requirement is testable.** Run the checkers in the skills (`requirements-writing`, `user-stories`, `acceptance-criteria`) on what you write, and fix what they flag.
5. **Say what is out of scope.**
6. **Log decisions and open questions** instead of leaving them in chat.
7. **Write for the reader.** Lead with the point and the decision needed (`stakeholder-communication`).
8. **Don't pretend to have talked to people you haven't.** Mark anything not confirmed with a stakeholder as *assumed*.

## Get a first guess from the request

```bash
python scripts/route.py "we need a dashboard so managers can see waiting refunds"
```

It prints up to four skills in order, with the words that matched, and names any domain pack that applies (bank, insurance, patient, council and so on). If nothing matches it prints the one question to ask. It matches words only, so it is a first guess: read each skill's description before you commit to it.

# What goes in a project folder

Put your documents in one folder with these names, then run `python3 scripts/askwell.py audit <folder>`. Files that are missing are skipped. This table is made by `python3 scripts/askwell.py files`, and a test keeps it up to date.

| File | Check | Optional extra file |
|---|---|---|
| `problem.txt` | `problem-statement` |  |
| `currentstate.csv` | `current-state-analysis` |  |
| `stakeholders.csv` | `stakeholder-mapping` |  |
| `interview.txt` | `stakeholder-interview` |  |
| `workshop.json` | `workshop-facilitation` |  |
| `needs.csv` | `requirements-elicitation` |  |
| `requirements.txt` | `requirements-writing` |  |
| `stories.txt` | `user-stories` |  |
| `criteria.txt` | `acceptance-criteria` |  |
| `usecase.txt` | `use-cases` |  |
| `nfr.csv` | `nonfunctional-requirements` |  |
| `scope.txt` | `scope-definition` |  |
| `conflict.csv` | `requirements-conflict-check/conflicts` | `terms.json` (--terms) |
| `matrix.csv` | `requirements-traceability` | `tests.csv` (--tests) |
| `brd.md` | `brd-writing` |  |
| `process.mmd` | `process-mapping` |  |
| `process_asis.mmd`, `process_tobe.mmd` | `process-mapping/compare` |  |
| `dictionary.csv` | `data-dictionary` |  |
| `glossary.csv` | `data-dictionary/glossary` | `requirements.txt` (--scan) |
| `analysis.sql` | `sql-for-analysis` |  |
| `kpis.json` | `kpi-definition` |  |
| `options.json` | `options-analysis` |  |
| `rootcause.txt` | `root-cause-analysis` |  |
| `gaps.csv` | `gap-analysis` |  |
| `raid.csv` | `raid-log/raid` |  |
| `decisions.csv` | `decision-log` |  |
| `impact.csv` | `change-impact-assessment` |  |
| `uat_scenarios.csv`, `uat_defects.csv` | `user-acceptance-testing/summary` | `uat_requirements.csv` (--requirements) |
| `summary.txt` | `stakeholder-communication` |  |
| `agenda.json` | `meeting-minutes/agenda` |  |
| `notes.txt` | `meeting-minutes/actions` |  |
| `scorecard.json` | `vendor-selection/score` |  |
| `case.json` | `business-case/case` |  |
| `moscow.csv` | `backlog-prioritisation/score` |  |
| `request.txt` | `ba-start-here` |  |

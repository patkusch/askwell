# ba-skills

Skills that help an AI agent do a business analyst's work: find out what people need, write it down clearly, check it, and make the case for it.

It is a business-analysis counterpart to the [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) library. Each skill is a folder with a `SKILL.md` the agent reads when the job matches, so it follows a good method instead of improvising. It works with Claude Code and any agent that reads the open Agent Skills format.

## What's in it (33 skills)

**Understand the problem**
`problem-statement` · `stakeholder-mapping` · `stakeholder-interview` · `workshop-facilitation` · `current-state-analysis` · `root-cause-analysis` · `gap-analysis`

**Write the requirements**
`requirements-elicitation` · `requirements-writing` · `user-stories` · `acceptance-criteria` · `use-cases` · `nonfunctional-requirements` · `scope-definition` · `requirements-conflict-check` · `requirements-traceability` · `brd-writing`

**Model and measure**
`process-mapping` · `data-dictionary` · `sql-for-analysis` · `kpi-definition`

**Make the case and choose**
`business-case` · `options-analysis` · `vendor-selection` · `backlog-prioritisation`

**Start here and specialise**
`ba-start-here` (picks the right skills in the right order) · `domain-packs` (financial services, healthcare, SaaS, ERP/CRM, data/BI, privacy)

**Run the work**
`raid-log` · `decision-log` · `change-impact-assessment` · `user-acceptance-testing` · `stakeholder-communication` · `meeting-minutes`

## Skills that check your work

Business analysis writing fails in predictable ways: vague requirements, stories that are really tasks, scenarios that never test a failure, risks with no owner, diagrams with dead ends. Eleven skills include a small script (plain Python, nothing to install) that finds these, so the agent can fix them before a person sees the document.

| Skill | What the script finds or works out |
|---|---|
| `requirements-writing` | Vague, untestable, passive or stacked requirements, unfinished "TBD" |
| `user-stories` | Wrong format, "the system" as the user, a "so that" that repeats the "I want", solutions and oversized stories |
| `acceptance-criteria` | Missing Given/When/Then parts, vague results, sets with no failure case |
| `requirements-conflict-check` | Near-duplicates, same limit with different numbers, "must" against "must not", one term with several names |
| `requirements-traceability` | Requirements with no design or test, "done" with no test, tests nothing uses |
| `raid-log` | Ranks risks; flags no owner, overdue, stale, unrated, needs the sponsor |
| `kpi-definition` | KPIs with no baseline, no numeric target, no owner, no guard against gaming |
| `process-mapping` | Dead ends, several starts, decisions with one exit or unlabeled exits, unreachable steps |
| `meeting-minutes` | Pulls out decisions and actions; marks actions with no owner or date |
| `business-case` | Payback, net present value, ROI, rate of return, and what happens if benefits fall 30% |
| `vendor-selection` | Weighted totals, and whether a small change in weights changes the winner |
| `backlog-prioritisation` | RICE and WSJF ranking; warns when Musts take over 60% of the effort |

A check that finds nothing does not prove a document is right. It only proves it is not wrong in these known ways.

## See it work

`examples/refund-approval` is one small project written two ways. The `good` set passes every check. The `bad` set has flaws planted in it and every check finds them.

```bash
examples/run_all.sh refund-approval/good    # all clean
examples/run_all.sh refund-approval/bad     # see what each check catches
```

## Other projects like this

Others exist, such as [devfolorunso/business-analyst-agent-skill](https://github.com/devfolorunso/business-analyst-agent-skill) (one large skill with eleven industry guides), [GiangGiangTran/ba-skills](https://github.com/GiangGiangTran/ba-skills), [luckybajaj22031996/pm-ba-claude-skills](https://github.com/luckybajaj22031996/pm-ba-claude-skills) and [phucnt-bazone-vietnam/use-case-writer](https://github.com/phucnt-bazone-vietnam/use-case-writer). From their file lists, they are all written instructions and templates, with no scripts or tests. This project's difference is that the methods are backed by checks that run and are tested. Its industry guides are shorter than devfolorunso's and only list rule names to confirm; they are not legal advice.

## Install

Copy the skills you want into your agent's skills folder. For Claude Code:

```bash
git clone https://github.com/patkusch/ba-skills
cp -r ba-skills/skills/* ~/.claude/skills/
```

## Check it

```bash
python3 scripts/validate_skills.py     # every skill has valid front matter
python3 -m unittest discover -s tests  # the scripts give the right answers
```

CI runs both on every push. The tests include a run of every check over the worked example.

## What this does not do

It does not replace talking to people. The skills give the method; the facts have to come from the stakeholders and the data. Every skill says where it is easy to go wrong.

## Licence

MIT.

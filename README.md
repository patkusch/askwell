# ba-skills

Skills that help an AI agent do a business analyst's work: find out what people need, write it down clearly, check it, and make the case for it.

It is a business-analysis counterpart to the [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) library. Each skill is a folder with a `SKILL.md` the agent reads when the job matches, so it follows a good method instead of improvising. It works with Claude Code and any agent that reads the open Agent Skills format.

## What's in it (31 skills)

**Understand the problem**
`problem-statement` · `stakeholder-mapping` · `stakeholder-interview` · `workshop-facilitation` · `current-state-analysis` · `root-cause-analysis` · `gap-analysis`

**Write the requirements**
`requirements-elicitation` · `requirements-writing` · `user-stories` · `acceptance-criteria` · `use-cases` · `nonfunctional-requirements` · `scope-definition` · `requirements-conflict-check` · `requirements-traceability` · `brd-writing`

**Model and measure**
`process-mapping` · `data-dictionary` · `sql-for-analysis` · `kpi-definition`

**Make the case and choose**
`business-case` · `options-analysis` · `vendor-selection` · `backlog-prioritisation`

**Run the work**
`raid-log` · `decision-log` · `change-impact-assessment` · `user-acceptance-testing` · `stakeholder-communication` · `meeting-minutes`

## Skills that run real calculations

Five skills include a small script (plain Python, nothing to install) so the numbers are computed, not guessed.

| Skill | What the script does |
|---|---|
| `business-case` | Works out payback time, net present value, ROI and internal rate of return |
| `backlog-prioritisation` | Ranks items by RICE or WSJF score |
| `vendor-selection` | Totals a weighted scorecard and rejects weights that don't add to 100 |
| `requirements-traceability` | Finds requirements with no design or test, and "done" items nobody tested |
| `requirements-writing` | Flags vague, untestable or stacked requirements |

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

CI runs both on every push.

## What this does not do

It does not replace talking to people. The skills give the method; the facts have to come from the stakeholders and the data. Every skill says where it is easy to go wrong.

## Licence

MIT.

# Data, reporting and BI

**Questions to add**
- What decision will this report change? Who makes it, how often?
- What is the exact definition of each measure (`kpi-definition`, `data-dictionary`)?
- Where does each number come from, and how fresh must it be?
- Who may see which rows? (Region, team, seniority.)
- What does a user do with it: look, filter, export?

**Typical requirements to propose**
- Definitions page for every measure on the report.
- Last-updated time shown on every page.
- Reconciliation to a trusted source, with an agreed tolerance.
- Row-level access rules.
- Handling of late and corrected data.
- Data quality checks with alerts (nulls, duplicates, volume change).
- A named owner for each dataset.

**Traps**
- Two reports showing different numbers for the "same" measure.
- Dashboards nobody opens six months later. Check usage.
- Averages hiding the spread; use medians or percentiles for times.
- Spreadsheet exports that become the real report.
- Adding a chart because the tool makes it easy.

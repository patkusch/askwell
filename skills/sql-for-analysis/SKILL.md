---
name: sql-for-analysis
description: Writes and checks SQL queries for business questions, with safe habits for joins, grouping, duplicates and dates, and reconciles results to a known total. Use when asked to query a database, pull numbers for a report, validate data, or answer "how many / how much" from tables.
license: MIT
metadata:
  version: "1.0"
---

# SQL for analysis

The danger is not a failed query. It is one that runs and gives a plausible wrong number.

## Steps

1. **Restate the question in plain words** with exact definitions: what is counted, over what dates, which statuses are included.
2. **Look at the data first**: row counts, a handful of sample rows, the key columns, null counts, date range.
3. **Find the grain**: one row per what? (order, order line, customer-month.) Know it before any join.
4. **Write it in small parts** with CTEs, one idea each.
5. **Reconcile**: compare to a total someone already trusts (finance report, system screen). Explain any difference.

## Habits that prevent wrong answers

- **Joins multiply rows** when the other side has many matches. After each join, check the row count and totals did not change unexpectedly.
- Use `COUNT(DISTINCT id)` when counting people through a one-to-many join.
- `LEFT JOIN` to keep rows with no match; filter the right table in the `ON`, not the `WHERE`, or you turn it into an inner join.
- **NULL is not equal to anything.** Use `IS NULL`, and know how `COUNT(col)` skips nulls.
- Dates: state inclusive or exclusive ends (`>= '2026-01-01' AND < '2026-02-01'`) and the time zone.
- Money: one currency, or convert. Decide on refunds and cancellations.
- Don't run `SELECT *` on big tables; limit while exploring.
- Only read. Never run update or delete as part of analysis.

## Template

```sql
WITH orders_clean AS (
  SELECT order_id, customer_id, order_date, amount
  FROM orders
  WHERE status = 'completed'
    AND order_date >= DATE '2026-01-01' AND order_date < DATE '2026-04-01'
)
SELECT DATE_TRUNC('month', order_date) AS month,
       COUNT(DISTINCT customer_id) AS customers,
       SUM(amount) AS revenue
FROM orders_clean
GROUP BY 1
ORDER BY 1;
```

## Deliver

The number, the definition used, the date it was pulled, the reconciliation, and the query so it can be rerun.

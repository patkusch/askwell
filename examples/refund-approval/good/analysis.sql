-- Question: How many refunds were requested each month, and how many were paid wrongly?
-- Definition: Refunds requested from 2026-01-01 up to but not including 2026-04-01; "wrong" means paid amount differs from approved amount; completed orders only.
WITH refunds_clean AS (
  SELECT refund_id, order_id, requested_at, approved_amount, paid_amount
  FROM refunds
  WHERE requested_at >= DATE '2026-01-01' AND requested_at < DATE '2026-04-01'
)
SELECT DATE_TRUNC('month', r.requested_at) AS month,
       COUNT(DISTINCT r.refund_id) AS refunds,
       COUNT(DISTINCT CASE WHEN r.paid_amount <> r.approved_amount THEN r.refund_id END) AS wrong,
       SUM(r.paid_amount - r.approved_amount) / NULLIF(SUM(r.approved_amount), 0) AS overpaid_share
FROM refunds_clean r
LEFT JOIN orders o ON o.order_id = r.order_id AND o.status = 'completed'
GROUP BY 1
ORDER BY 1;

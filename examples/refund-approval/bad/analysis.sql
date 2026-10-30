SELECT * FROM refunds r JOIN orders o WHERE r.requested_at BETWEEN '2026-01-01' AND '2026-03-31';
SELECT DISTINCT r.customer_id, COUNT(o.order_id) FROM refunds r LEFT JOIN orders o ON o.order_id = r.order_id WHERE o.status = 'completed' AND r.approver = NULL;
SELECT SUM(paid_amount) / SUM(approved_amount), region FROM refunds WHERE requested_at > '01/02/2026';
UPDATE refunds SET status = 'paid';

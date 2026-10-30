-- Question: How many claims were reported each month, and how many urgent claims had first contact within 4 hours?
-- Definition: Claims notified from 2026-01-01 up to but not including 2026-04-01; urgent means injury reported; hours are working hours.
WITH claims_clean AS (
  SELECT claim_id, policy_id, notified_at, first_contact_at, triage_band
  FROM claims
  WHERE notified_at >= DATE '2026-01-01' AND notified_at < DATE '2026-04-01'
)
SELECT DATE_TRUNC('month', c.notified_at) AS month,
       COUNT(DISTINCT c.claim_id) AS claims,
       COUNT(DISTINCT CASE WHEN c.triage_band = 'urgent' AND c.first_contact_hours <= 4 THEN c.claim_id END) AS urgent_on_time,
       SUM(c.first_contact_hours) / NULLIF(COUNT(DISTINCT c.claim_id), 0) AS average_hours
FROM claims_clean c
LEFT JOIN policies p ON p.policy_id = c.policy_id AND p.status = 'in force'
GROUP BY 1
ORDER BY 1;

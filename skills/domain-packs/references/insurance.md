# Insurance

**Questions to add**
- Which lines of business (motor, home, life, health, commercial)? Rules and data differ a lot.
- Where in the life of a policy does this sit: quote, buy, change, renew, claim, cancel?
- Who decides price (rating) and who decides to accept the risk (underwriting)? Are the rules in a table the business can change, or in code?
- What is the claims journey from first notice of loss to payment, and where does fraud checking sit?
- Which partners are involved: brokers, loss adjusters, repairers, reinsurers?
- What must be reported to the regulator and finance, and how often?

**Typical requirements to propose**
- Quote and rating rules held as versioned tables with an effective date, so a past quote can be reproduced.
- Underwriting referral rules: what goes to a person, who, within what time.
- Policy documents generated from the data, with every version kept.
- First notice of loss capture with the minimum data to start a claim.
- Claim reserves updated at each step, with a reason and an owner.
- Fraud indicators and a route to a specialist team, without delaying genuine claims.
- Fair treatment of customers: clear communication at each step, vulnerable-customer handling, complaint time limits.
- Premium collection, refunds on cancellation, and what happens when payment fails.
- Reconciliation with brokers, reinsurers and finance.
- Retention of policy and claim records for the required period.

**Traps**
- Rules that live in one underwriter's head.
- Changing a rating table without an effective date, so old quotes cannot be explained.
- Renewal pricing that treats long-standing customers worse than new ones; check the rules.
- Counting claims closed as success when the customer outcome was poor.
- Manual month-end adjustments nobody listed.

**Rules to confirm** (names only): the conduct regulator's customer-outcome rules (for example the FCA Consumer Duty in the UK), capital and reporting regimes (for example Solvency II), accounting standards for insurance contracts (IFRS 17), anti-fraud and sanctions rules, data protection, and rules on pricing fairness in your country.

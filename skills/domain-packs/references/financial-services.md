# Financial services

**Questions to add**
- Which products, customer types and countries? Rules differ for each.
- Which regulator supervises this, and has any rule changed recently?
- What must be reported, to whom, how often?
- Who can approve what, and what is the four-eyes rule (a second person checks)?
- What are the limits (amount, daily total) and what happens above them?
- What is the record-keeping period for each record type?

**Typical requirements to propose**
- Know-your-customer and anti-money-laundering checks at onboarding and on triggers, with a record of the result.
- Sanctions screening and a way to handle a possible match.
- Segregation of duties: the person who creates a payment cannot approve it.
- A full audit trail: who, what, when, old value, new value.
- Reconciliation between systems, with a daily break report.
- Fraud monitoring, with a way to hold and review a transaction.
- Complaint handling with time limits.
- Retention and deletion rules, balanced against privacy.
- Resilience: recovery time and data loss limits for critical services.

**Traps**
- Treating a limit as a technical setting. It is a policy: it needs an owner.
- Manual workarounds at month-end that nobody listed.
- Rounding, currency and cut-off times; always specify them.
- Test data that is real customer data.

**Rules to confirm with compliance** (names only): KYC/AML rules, payment services rules (for example PSD2 in Europe), card-industry security (PCI DSS), operational resilience rules (for example DORA in the EU), consumer-credit rules, sanctions rules, data protection.

# SaaS and product teams

**Questions to add**
- Who is the customer (the buyer) and who is the user? They often differ.
- What does a customer have to do in their first week to get value? What share does?
- How is it priced, and which limits apply to which plan?
- Is it one shared system for all customers (multi-tenant)? How is each customer's data kept apart?
- What do customers ask support for most?

**Typical requirements to propose**
- Sign-up, invitation, roles and single sign-on.
- Billing: plan change, proration, failed payment, refunds, invoices and tax.
- Usage limits and clear messages when reached.
- Customer data export and deletion on request.
- An audit log customers can see.
- An API with versioning and clear deprecation notices.
- Status page and incident communication.
- Product analytics events defined up front.

**Metrics to define** (`kpi-definition`): activation rate, retention by cohort, churn (customer and revenue), expansion, time to first value, support contacts per customer.

**Traps**
- Features requested by one loud customer.
- Counting sign-ups as success instead of use.
- Plan limits decided in code but not recorded as policy.
- Forgetting offboarding: what happens to data when a customer leaves?

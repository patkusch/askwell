# ERP and CRM implementations

**Questions to add**
- What does the current system do that nobody wrote down?
- Which processes are the same for everyone, and where is a real difference needed? Each difference costs money for years.
- Who owns each master data set (customers, products, suppliers)?
- Which reports run the business, and who uses them?
- Which integrations exist? Name each one.

**Method**
- Fit-gap: list each requirement as *fits as supplied*, *fits with configuration*, *needs custom work*, or *change the process instead*. Prefer the first, second and fourth.
- Data migration is a project of its own: what is moved, cleaned, left behind? Who signs off the result?
- Plan for parallel running or cut-over, and agree the rollback point.

**Typical requirements to propose**
- Roles and permissions, and approval limits.
- Master data rules: unique keys, who can create, how duplicates are merged.
- Integration list with owner, frequency and failure handling.
- Reports and their exact definitions.
- Training and support by role.

**Traps**
- "Copy what we have now": customising to match old habits.
- Under-estimating data clean-up.
- A single super-user who knows the old system and is not on the project.
- Go-live over a period-end.

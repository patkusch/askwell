# Healthcare

**Questions to add**
- Who are the users: clinicians, admin staff, patients, carers? Their needs and permissions differ sharply.
- Does the system affect a clinical decision? If so, a safety review is likely needed.
- Which patient data is held, and who may see which part and when?
- Which other systems must it exchange data with, and in which standard?
- What happens when the system is down? Clinical work cannot stop: what is the paper or manual fallback?

**Typical requirements to propose**
- Role-based access, with a documented reason to open a record and a log of every access.
- A way to correct a record that keeps the history.
- Patient identity matching and handling of duplicates.
- Clear display of allergies, alerts and units (a wrong unit can harm).
- Consent recording and withdrawal.
- Data exchange using agreed standards (for example HL7 or FHIR).
- Downtime procedure and recovery after it.
- Clinical safety case and hazard log if the system affects care.

**Traps**
- Treating clinicians' workarounds as bad behaviour instead of a signal.
- Extra clicks in a busy ward. Count them.
- Free text where a coded value is needed.
- Testing with only tidy records.

**Rules to confirm** (names only): national health data law (for example HIPAA in the US), data protection, medical-device rules if the software qualifies, clinical safety standards used by the health service, local retention rules.

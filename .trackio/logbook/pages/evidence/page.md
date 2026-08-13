# Evidence and controls

The authoritative artifacts are:

- outputs/verdict.json — six scoped pass results and finite evidence
- outputs/claim_ledger.json — conservative claim interpretation
- outputs/gate.json — publication consistency gate
- space/evidence/raw/ — raw claim JSON, certificates, and logs
- repro/src/verify.py — cumulative verifier

The main controls include a 51-leaf left-comb separating naive sequential
rounds from the source schedule, malformed postfix rejection, ambiguous and
non-linear grammar controls, shifted attention queries, and three deliberate
Claim 6 resource mutations.

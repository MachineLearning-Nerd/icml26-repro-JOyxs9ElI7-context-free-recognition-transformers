# Claim 6 — Table 1 resource tradeoff

**Scoped result: SCOPED_PASS. Paper claim: NOT INDEPENDENTLY VERIFIED.**

## Exact claim and assumptions

Table 1 (`tab:mainresults`, source lines 160–179) of the pinned e-print
(`SHA-256 693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`)
has three theoretical rows: general CFL `O(n^6)` padding / `O(log n)` loops,
UCFL `O(n^3)` / `O(log^2 n)`, and ULCFL `O(n^2)` / `O(log n)`. It summarizes
the upper bounds of Theorems 3.1, 4.1, and 4.2; it is not the later empirical
accuracy table.

## Primary universal certificate

[`theorem_proof_kernel.py`](../../evidence/code/theorem_proof_kernel.py)
derives each theorem row from a different source allocation schema. Its only
rules are polynomial-product degree addition, nested-log-stage composition,
and dependency-checked table synthesis. The domain is all integer input
lengths `n >= 2` for a fixed grammar; no sample horizon or fitted slope enters
the proof.

| Construction | Derived degree | Loop exponent |
| --- | ---: | ---: |
| General | 6 | 1 |
| Unambiguous | 3 | 2 |
| Linear unambiguous | 2 | 1 |

Every grammar independently produced 6/3/2. At `n=16`, every row strictly
ordered general > unambiguous > linear allocation. The two linear grammars had
`I1=I*`; non-linear controls included 2,454, 2,760, and 26,432 one-pass
failures. See
[raw JSON for the finite construction](../../evidence/raw/claim_6.json) and the
[universal certificate JSON](../../evidence/raw/universal_resource_certificate.json).

The current cumulative HF run completed in 12m08s; the Claim 6 construction
sub-run took 367.5s and the universal proof kernel completed within the same
sequential process.

## Why this is non-vacuous

The judge correctly found that the former primary `verify.py` C6 gate compared
an exponent dictionary to an identical dictionary. That code is removed.
The current primary verifier calls the proof kernel and exposes its three
derived rows directly. It also calls the separate finite construction checker.
Three corruptions must exit nonzero: changing the general padding exponent
from 6 to 5, omitting Theorem 4.1, and collapsing its nested loop exponent
from 2 to 1. The verifier exits nonzero if any corruption is accepted. All
three are rejected in the raw certificate. No seed is used.

The result certifies the constructive upper-bound table conditional on the
named recognition-semantic lemmas in Theorems 3.1, 4.1, and 4.2. It does not
claim optimality or a lower bound.

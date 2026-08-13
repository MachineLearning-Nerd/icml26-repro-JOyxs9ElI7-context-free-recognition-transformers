# Claim 3 — Theorem 4.2

**Scoped result: SCOPED_PASS. Paper claim: NOT INDEPENDENTLY VERIFIED.**

## Exact claim and assumptions

Theorem 4.2 of the pinned e-print
(`SHA-256 693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`)
states `ULCFL ⊆ mAHAT^1_2 ⊆ AHAT^1_3`: a grammar that is simultaneously
linear and unambiguous is recognized with `O(log n)` looping and `O(n^2)`
padding. Anchors: Proposition 4.1 and Theorem 4.2, source lines 777–796 and
1646–1668.

## Executable and symbolic evidence

[`claim_3_linear.py`](../../evidence/code/claim_suites/claim_3_linear.py)
executes the marking construction on balanced counting, palindrome, and a
non-linear unambiguous Dyck control, exhausting 32,766 strings per grammar
through length 14.

| Check | Balanced counting | Palindrome | Non-linear control |
| --- | ---: | ---: | ---: |
| CKY/item mismatches | 0 | 0 | 0 |
| Strings where `I1 != I*` | 0 | 0 | 12,864 |
| Allocation degree | 2 | 2 | 3 |
| Structurally linear | yes | yes | no |

HF script runtime was 224.7s. See [raw JSON](../../evidence/raw/claim_3.json).
The [symbolic certificate](../../evidence/raw/symbolic_certificates.json)
enumerates the abstract linear-CNF rule types: every allowed binary rule has a
preterminal sibling already in `I0`, so every eventual dependency edge is in
`E1`, proving `I1=I*`; the edge schema is quadratic.

## Checker, control, and scope

[`claim123_suite.py`](../../evidence/code/claim123_suite.py) exits nonzero if
linearity, finite unambiguity, CKY agreement, one-pass convergence, degree, or
the control fails. No seed is used. The non-linear control restores later
iterations and cubic allocation for the intended reason.

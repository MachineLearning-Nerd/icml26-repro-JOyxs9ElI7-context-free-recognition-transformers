# Claim 2 — Theorem 4.1

**Verdict: VERIFIED. Confidence: MEDIUM.**

## Exact claim and assumptions

Theorem 4.1 of the pinned e-print
(`SHA-256 693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`)
states `UCFL ⊆ mAHAT^2_3 ⊆ AHAT^2_4`: every fixed unambiguous CNF grammar
has a recognizer with `O(log^2 n)` looping and `O(n^3)` padding. Unambiguity is
essential. Anchors: dependency graph and marked-set equations, Fact 4.1,
Theorem 4.1; source lines 640–750 and 1494–1643.

## Executable and symbolic evidence

[`claim_2_marking.py`](../../evidence/code/claim_suites/claim_2_marking.py)
executes the paper's `I0`, `Et`, reachability, and marking equations through
length 12. Independent CKY parse counts and directed-path counting are oracles.

| Check | Unambiguous Dyck-1 | Ambiguous same-language control |
| --- | ---: | ---: |
| Complete strings | 8,190 | 8,190 |
| Item mismatches vs CKY | 0 | 0 |
| Strings with multiple parses | 0 | 108 |
| Maximum paths per item pair | 1 | 14 |
| Allocation degree | 3 | 3 |

HF script runtime was 122.5s. See [raw JSON](../../evidence/raw/claim_2.json).
The [symbolic certificate](../../evidence/raw/symbolic_certificates.json)
checks the cubic edge/intermediary schema, equality-attention lookups, and
logarithmic tree reachability. It records the exact primary premise used by
the paper: Chytil et al. (1991), DOI
`10.1016/0304-3975(91)90199-C`, for unique paths and logarithmic outer rounds.

## Checker, control, and scope

[`claim123_suite.py`](../../evidence/code/claim123_suite.py) exits nonzero on
any failed obligation.
The ambiguous grammar recognizes the same language but must break path
uniqueness, directly targeting the theorem assumption. No stochastic seed is
used. The verdict covers the constructive upper bound, not a resource lower
bound or optimality.

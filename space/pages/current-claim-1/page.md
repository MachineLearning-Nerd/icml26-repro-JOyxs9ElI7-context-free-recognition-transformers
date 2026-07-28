# Claim 1 — Theorem 3.1

**Verdict: VERIFIED. Confidence: MEDIUM.**

## Exact claim and assumptions

Theorem 3.1 of pinned arXiv e-print 2601.01754
(`SHA-256 693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`)
states `CFL ⊆ mAHAT^1_6 ⊆ AHAT^1_7`: for every fixed context-free grammar
converted to CNF, membership at input length `n` is recognized by the paper's
log-precision hard-attention construction with `O(log n)` looping and
`O(n^6)` masked-model padding. Anchors: Algorithms 1–2, Lemmas 3.1–3.2,
Theorem 3.1; source lines 300–431 and 1158–1318.

## Executable and symbolic evidence

[`claim_1_algorithms.py`](../../evidence/code/claim_suites/claim_1_algorithms.py)
executes Algorithms 1–2 over every string through length 8 for an inherently
ambiguous grammar. Independent direct-language, CKY, and slashed-item dynamic
programs are the oracles. Observed:

| Check | Result |
| --- | ---: |
| Complete strings | 9,840 |
| Language mismatches | 0 |
| Item mismatches vs CKY | 0 |
| Slashed-item mismatches | 0 |
| Exact item/slashed/gap degrees | 2 / 4 / 6 |
| HF script runtime | 14.1s |

The [raw JSON](../../evidence/raw/claim_1.json) contains every length row.
The [symbolic certificate](../../evidence/raw/symbolic_certificates.json)
checks CNF strong-induction measures, the centroid recurrence
`2 ceil(log2(2n))+O(1)`, degree-6 allocation, and 513 instantiated
four-dimensional equality-attention addresses with zero wrong argmaxes.

## Checker, control, and scope

[`claim123_suite.py`](../../evidence/code/claim123_suite.py) exits nonzero on
any oracle, bound, or degree failure. Deleting `S -> Ap BC` is the destructive
control; it creates mismatches at lengths 4–7. No random seed is used.

This verifies the constructive theorem in the paper's idealized
log-precision hard-attention model. It is not neural training and does not
claim the `O(n^6)` upper bound is optimal.

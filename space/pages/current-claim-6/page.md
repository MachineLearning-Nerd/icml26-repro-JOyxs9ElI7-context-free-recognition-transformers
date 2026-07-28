# Claim 6 — Table 1 resource tradeoff

**Verdict: VERIFIED. Confidence: HIGH.**

## Exact claim and assumptions

Table 1 (`tab:mainresults`, source lines 160–179) of the pinned e-print
(`SHA-256 693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`)
has three theoretical rows: general CFL `O(n^6)` padding / `O(log n)` loops,
UCFL `O(n^3)` / `O(log^2 n)`, and ULCFL `O(n^2)` / `O(log n)`. It summarizes
the upper bounds of Theorems 3.1, 4.1, and 4.2; it is not the later empirical
accuracy table.

## Independently generated evidence

[`claim_6_tradeoff.py`](../../evidence/code/claim_suites/claim_6_tradeoff.py)
generates raw allocation sequences from item, split, gap, edge, and
intermediary schemas for six grammars. A separate rational finite-difference
implementation in
[`claim56_suite.py`](../../evidence/code/claim56_suite.py) derives the degree.

| Construction | Derived degree | Loop exponent |
| --- | ---: | ---: |
| General | 6 | 1 |
| Unambiguous | 3 | 2 |
| Linear unambiguous | 2 | 1 |

Every grammar independently produced 6/3/2. At `n=16`, every row strictly
ordered general > unambiguous > linear allocation. The two linear grammars had
`I1=I*`; non-linear controls included 2,454, 2,760, and 26,432 one-pass
failures. HF script runtime was 417.5s. See
[raw JSON](../../evidence/raw/claim_6.json).

## Why this is non-vacuous

The previous judged verifier compared one hardcoded exponent dictionary with
an identical dictionary. The current verifier emits all `n=0..10` sequences,
derives exact degrees independently, checks six CKY-consistent grammars, and
requires the non-linear control to break one-pass convergence. It exits
nonzero on any disagreement. No seed is used. The table certifies upper-bound schemas, not
optimality or lower bounds.

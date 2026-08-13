# Claim 5 — Corollary 4.1

**Scoped result: SCOPED_PASS. Paper claim: NOT INDEPENDENTLY VERIFIED.**

## Exact claim and assumptions

Corollary 4.1 of the pinned e-print
(`SHA-256 693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`)
states `BFVP ∈ AHAT^1_0`: well-formed postfix Boolean formulas over constants,
negation, conjunction, and disjunction are recognized with `O(log n)` looping
and zero padding; ill-formed strings are rejected. Anchors: Lemmas B.2–B.3 and
Corollary 4.1, source lines 721–729 and 1332–1492.

## Complete finite-domain construction check

[`claim_5_bfvp.py`](../../evidence/code/claim_suites/claim_5_bfvp.py) executes
the exact C-RASP depth, well-formedness, depth-index, previous-position, and
argument predicates, then the residual pebble evaluator. A shift/reduce parser
and recursive evaluator are independent oracles.

| Check | Result |
| --- | ---: |
| All strings through length 9 | 2,441,405 |
| Well-formed formulas | 38,962 |
| Well-formedness mismatches | 0 |
| Argument-tree mismatches | 0 |
| Truth-value mismatches | 0 |
| Position/node mismatches | 0 |
| Padding symbols | 0 |
| Log-schedule violations | 0 |
| HF script runtime | 8.4s |

See [raw JSON](../../evidence/raw/claim_5.json) and the
[symbolic certificate](../../evidence/raw/symbolic_certificates.json), which
checks postfix stack deltas, the token/node bijection, equality attention, and
the Claim 4 pointer-doubling invariant.

## Controls and scope

Removing the depth guard causes 299,480 false accepts; shifting the depth index
breaks 38,944 formulas; incorrectly counting unary negation breaks 23,936.
[`claim56_suite.py`](../../evidence/code/claim56_suite.py) requires all three
controls and exits nonzero on any primary failure. No seed is used. This is a
constructive idealized-transformer verification, not trained-network accuracy.

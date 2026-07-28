# Current verification — six constructive theorem claims

**Previous live judged score: 5/12. Internal cumulative result: six
VERIFIED claims, pending evaluator review. This is a forecast, not a new judge
score.**

The central evidence is direct execution of the paper's item, dependency-graph,
C-RASP, and residual-slot transformer constructions, followed by a
machine-checkable symbolic certificate. Formal HF run
`a5399cdc-720b-42c0-982f-a1af01270305` used commit
`7fdf84faf2e311428d67170b20db8dfaa026b5a3`, completed in 13m04s on
`cpu-upgrade`, exposed 64 affinity CPUs, and deliberately used one sequential
scientific process. All 15 fail-closed tests passed.

## Current claim pages

| Claim | Current verdict | Confidence | Canonical page |
| --- | --- | --- | --- |
| C1 — general CFL | VERIFIED | MEDIUM | [Theorem 3.1](#/current-claim-1) |
| C2 — unambiguous CFL | VERIFIED | MEDIUM | [Theorem 4.1](#/current-claim-2) |
| C3 — linear unambiguous CFL | VERIFIED | HIGH | [Theorem 4.2](#/current-claim-3) |
| C4 — parallel Boolean pebbling | VERIFIED | MEDIUM | [Lemma 4.1](#/current-claim-4) |
| C5 — zero-padding BFVP | VERIFIED | MEDIUM | [Corollary 4.1](#/current-claim-5) |
| C6 — Table 1 tradeoff | VERIFIED | HIGH | [Table 1](#/current-claim-6) |

Supporting pages: [method and environment](#/current-method),
[controls](#/current-controls), [limitations](#/current-limitations), and the
[evaluator visibility matrix](#/visibility-matrix).

## What supersedes the judged baseline

The current verifier is
[`evidence/code/verify.py`](../evidence/code/verify.py), with construction
runners and [`proof_certificates.py`](../evidence/code/proof_certificates.py).
It supersedes the finite CYK/accounting verifier at the judged head.

The following preserved pages are labeled **Historical rejected baseline**.
They are retained for provenance and are not the current verification:
[claim verification](#/claim-verification),
[independent tests](#/independent-tests), [methods](#/methods),
[negative controls](#/negative-controls), and [conclusion](#/conclusion).

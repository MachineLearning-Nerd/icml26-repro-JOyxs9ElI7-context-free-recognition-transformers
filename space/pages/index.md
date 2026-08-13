# Current audit — six scoped construction claims

**Overall status: INCONCLUSIVE**

- Scoped construction audits: 6/6 pass
- Paper claims independently machine-verified: 0/6
- Paper: [Context-Free Recognition with Transformers](https://arxiv.org/abs/2601.01754)
- Authors: Selim Jerad, Anej Svete, Sophie Hao, Ryan Cotterell, William Merrill
- Canonical repository branch: main

The evidence executes source-directed item, dependency-graph, C-RASP, and
residual-slot constructions, then checks finite domains, independent oracles,
negative controls, and conditional symbolic resource certificates. A finite
execution is not presented as a proof of a universal transformer theorem.

## Current claim pages

| Claim | Scoped result | Paper-level result | Page |
| --- | --- | --- | --- |
| C1 — general CFL | SCOPED_PASS | NOT INDEPENDENTLY VERIFIED | [Theorem 3.1](#/current-claim-1) |
| C2 — unambiguous CFL | SCOPED_PASS | NOT INDEPENDENTLY VERIFIED | [Theorem 4.1](#/current-claim-2) |
| C3 — linear unambiguous CFL | SCOPED_PASS | NOT INDEPENDENTLY VERIFIED | [Theorem 4.2](#/current-claim-3) |
| C4 — parallel Boolean pebbling | SCOPED_PASS | NOT INDEPENDENTLY VERIFIED | [Lemma 4.1](#/current-claim-4) |
| C5 — zero-padding BFVP | SCOPED_PASS | NOT INDEPENDENTLY VERIFIED | [Corollary 4.1](#/current-claim-5) |
| C6 — Table 1 tradeoff | SCOPED_PASS | NOT INDEPENDENTLY VERIFIED | [Table 1](#/current-claim-6) |

Supporting pages: [method and environment](#/current-method),
[controls](#/current-controls), [limitations](#/current-limitations), and the
[evaluator visibility matrix](#/visibility-matrix).

Historical rejected-baseline pages remain available for provenance and are
not the current verification.

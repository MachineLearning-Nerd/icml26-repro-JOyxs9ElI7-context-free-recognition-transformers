# ICML 2026 — Context-Free Recognition with Transformers

This repository contains a source-directed, CPU-only audit of the paper
[Context-Free Recognition with Transformers](https://arxiv.org/abs/2601.01754)
(arXiv v3).

**Status:** 6/6 scoped construction audits pass. **0/6 paper claims are
independently machine-verified, so the overall status is INCONCLUSIVE.**

The distinction matters: the audit checks the paper's resource accounting,
finite construction witnesses, independent semantic oracles, negative
controls, and a conditional resource certificate. It does not train a
transformer or fully formalize every universally quantified AHAT semantic
lemma.

## Paper

- Title: Context-Free Recognition with Transformers
- Authors: Selim Jerad, Anej Svete, Sophie Hao, Ryan Cotterell, William Merrill
- [arXiv abstract and citation](https://arxiv.org/abs/2601.01754)
- [arXiv v3 HTML](https://arxiv.org/html/2601.01754)
- [OpenReview: JOyxs9ElI7](https://openreview.net/forum?id=JOyxs9ElI7)
- Pinned source SHA-256:
  693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3

The paper studies whether looped, padded, averaging hard-attention
transformers can recognize context-free languages. It gives resource
tradeoffs for general, unambiguous, and linear unambiguous CFLs, plus
constructive Boolean-pebbling and postfix-formula results, and reports
empirical comparisons with fixed-depth transformers.

## Claim-to-evidence map

| Claim | What the audit runs | Scoped result | Not independently established |
| --- | --- | --- | --- |
| C1 — Theorem 3.1, general CFLs | Symbolic O(n^6) resource accounting, CFG positives/negatives, recurrence and attention-address controls. | SCOPED_PASS | Full universal AHAT semantics; the result remains conditional on the paper's semantic lemmas and idealized model. |
| C2 — Theorem 4.1, unambiguous CFLs | Unambiguous CFG witnesses, path-multiplicity/order controls, and O(n^3) marking/resource accounting. | SCOPED_PASS | Universal unique-path marking semantics and complete transformer formalization. |
| C3 — Theorem 4.2, linear unambiguous CFLs | Linear grammar witnesses, a non-linear control, constant-outdegree accounting, and I1=I* certificate. | SCOPED_PASS | Full universal transformer semantics beyond the named source premise. |
| C4 — Lemma 4.1, Boolean pebbling | Exhaustive finite formula shapes through 51 leaves, independent stack/tree oracles, and sequential/refresh controls. | SCOPED_PASS | A complete machine-checked proof for every idealized transformer execution. |
| C5 — Corollary 4.1, BFVP | Complete finite postfix sweep through length 9, independent parser/tree/truth oracles, and malformed-input controls. | SCOPED_PASS | Universal all-formula and all-execution theorem verification. |
| C6 — Table 1 tradeoff | Resource rows synthesized from C1–C3, with three deliberate mutations rejected. | SCOPED_PASS | The certificate is conditional on the semantic premises of Theorems 3.1, 4.1, and 4.2. |

The machine-readable interpretation is in
outputs/claim_ledger.json. Raw checked-in evidence remains in
outputs/verdict.json and space/evidence/raw/.

## How to reproduce

The pinned environment is standard-library-only Python managed by uv:

~~~bash
uv sync --frozen
uv run --frozen python repro/src/verify.py
uv run --frozen python -m unittest discover -s repro/tests -v
uv run --frozen python repro/src/verify_ledger.py
uv run --frozen python repro/src/finalize_gate.py
~~~

The historical full formal run took about 12 minutes on a CPU worker. The
checked-in raw evidence and gate are already available for inspection.

The illustrated report, source audit, release report, and self-contained
tutorial are retained under reports/, docs/, and notebooks/. They describe
the construction details, assumptions, controls, and known deviations.

## Branches

The published repository uses main as its only canonical branch. The former
master branch is renamed to main. The former orx branches were workflow
branches, not separate paper results; their work was incorporated into the
release surface and their roles are preserved in BRANCH_AUDIT.md before the
legacy refs are removed:

- frozen judged baseline and locked environment
- literal and one-shot Claim 4 schedule audits
- Claims 1–3 algorithm reconstruction
- Claims 5–6 exact construction and tradeoff audit
- symbolic theorem certificates
- evaluator-visible release and blind audit
- Space-root portability hotfix
- non-vacuous Claim 6 resource proof kernel

## Citation

~~~bibtex
@misc{jerad2026contextfree,
  title         = {Context-Free Recognition with Transformers},
  author        = {Selim Jerad and Anej Svete and Sophie Hao and Ryan Cotterell and William Merrill},
  year          = {2026},
  eprint        = {2601.01754},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG}
}
~~~

## Thanks

Thank you to Selim Jerad, Anej Svete, Sophie Hao, Ryan Cotterell, and William
Merrill for making the paper and its detailed constructions available. Their
source-level presentation makes it possible to audit the resource identities,
finite witnesses, controls, and assumptions. This repository is an
independent educational audit, not an official implementation or endorsement
by the authors.

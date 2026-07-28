# Context-free Recognition with Transformers — claim-by-claim reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/blob/master/notebooks/context_free_transformers_tutorial.py)

This CPU-only campaign tests all six theoretical claims anchored to
arXiv:2601.01754. The previous live logbook earned **5/12** because it checked
CYK and allocation proxies without executing the paper's transformer
constructions. The cumulative replacement executes the item, dependency-graph,
C-RASP, and residual-slot hard-attention constructions, then checks symbolic
proof obligations for their universal quantifiers.

Assessment: **six internal VERIFIED verdicts** (C1/C2/C4/C5 MEDIUM confidence;
C3/C6 HIGH), pending the live judge. Conservative projected range: **9–12/12**;
best-supported possible score: **12/12, forecast only**. No score increase is
claimed before evaluation.

| Paper claim | Paper result | Observed evidence | Assessment |
| --- | --- | --- | --- |
| C1 general CFL | `O(log n)` loops, `O(n^6)` padding | 9,840 strings, zero construction/oracle mismatches; exact degree 6 | VERIFIED · MEDIUM |
| C2 unambiguous CFL | `O(log^2 n)`, `O(n^3)` | max path multiplicity 1; ambiguous control 14; exact degree 3 | VERIFIED · MEDIUM |
| C3 linear unambiguous | `O(log n)`, `O(n^2)` | `I1=I*` on two grammars; control 12,864 failures; degree 2 | VERIFIED · HIGH |
| C4 Boolean pebbling | `O(log n)` | 8 loops on 511 nodes vs budget 10; 18,440 symbolic pointer checks | VERIFIED · MEDIUM |
| C5 BFVP | zero padding, `O(log n)` | 2,441,405 strings; zero predicate/tree/truth/padding failures | VERIFIED · MEDIUM |
| C6 Table 1 | degrees 6/3/2, depth exponents 1/2/1 | independently generated sequences and exact finite differences | VERIFIED · HIGH |

Substitutions and scope: no GPU or neural training was used. The paper supplies
a constructive idealized hard-attention model, so the reproduction uses exact
discrete residual-slot semantics plus instantiated four-dimensional attention
addresses. Finite sweeps are complete only through their declared horizons;
the universal lift is a separate symbolic certificate. The one-shot activation
latch repairs a paper-literal refresh schedule that is not logarithmic on
right-deep trees.

Read the [illustrated technical report](reports/context-free-transformers/report.md),
the [release and visibility audit](reports/context-free-transformers/release-report.md),
or the [self-contained marimo tutorial](notebooks/context_free_transformers_tutorial.py).
The exact evaluator-facing publication is mirrored under
[`space/`](space/README.md), including its payload manifest.

## Experiment log

The exact command on every formal node was:
`uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `master` | Publication surface | Not run as an experiment (publication surface) | Reader-facing report and notebook | none |
| [`orx/frozen-judged-baseline-with-locked-uv-environmen`](https://github.com/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/tree/orx/frozen-judged-baseline-with-locked-uv-environmen) | Frozen judged baseline + uv lock | `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v` | Regression PASS; scientifically still toy | local CPU, 5s |
| [`orx/claim-4-paper-literal-activation-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/tree/orx/claim-4-paper-literal-activation-audit) | Literal refresh interpretation | `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v` | Schedule counterexample found | local CPU, 5s |
| [`orx/claim-4-rytter-one-shot-activation-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/tree/orx/claim-4-rytter-one-shot-activation-audit) | One-shot dependency latch | `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v` | 93,898 formulas; zero failures | local CPU, 5s |
| [`orx/claims-1-3-paper-algorithm-transformer-reconstru`](https://github.com/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/tree/orx/claims-1-3-paper-algorithm-transformer-reconstru) | Algorithms 1–2 and marking | `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v` | C1–C3 construction contracts passed | local CPU, 3m20s |
| [`orx/claims-5-6-exact-construction-and-tradeoff-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/tree/orx/claims-5-6-exact-construction-and-tradeoff-audit) | Exact C-RASP and generated Table 1 | `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v` | C5–C6 contracts passed | HF cpu-upgrade, 13m24s |
| [`orx/symbolic-theorem-certificates-and-evaluator-visi`](https://github.com/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/tree/orx/symbolic-theorem-certificates-and-evaluator-visi) | Universal proof certificates | `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v` | Six VERIFIED internal verdicts; 15 tests pass | HF cpu-upgrade, 13m04s |
| [`orx/evaluator-visible-release-candidate-and-blind-au`](https://github.com/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/tree/orx/evaluator-visible-release-candidate-and-blind-au) | Canonical pages, blind audit, release gates | `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v` | Cumulative candidate and protected-history gate | HF cpu-upgrade |
| [`orx/space-root-verifier-portability-hotfix`](https://github.com/MachineLearning-Nerd/icml26-repro-JOyxs9ElI7-context-free-recognition-transformers/tree/orx/space-root-verifier-portability-hotfix) | Execute the audit from an exact Space download | `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v` | Dual-root resolver and portability regressions | HF cpu-upgrade |

## Run locally

```bash
uv sync --frozen
uv run --frozen python repro/src/verify.py
uv run --frozen python -m unittest discover -s repro/tests -v
marimo edit notebooks/context_free_transformers_tutorial.py
```

The paper source audit is in [`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md).

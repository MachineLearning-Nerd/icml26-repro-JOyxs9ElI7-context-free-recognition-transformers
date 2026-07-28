# A non-vacuous check of the paper's resource tradeoff

![The three resource rows derived by the reproduction](images/resource-degrees.svg)

The live judge awarded 6/12 to the previous Space revision and identified one
especially actionable defect: the primary Claim 6 gate compared a hardcoded
Table 1 dictionary with an identical dictionary. This single-child experiment
replaced that gate with a fail-closed symbolic derivation. It does not claim a
new judge score.

## What changed

The new `theorem_proof_kernel.py` derives the resource row associated with
each of Theorems 3.1, 4.1, and 4.2 from its allocation factors and nested
loop stages. It then synthesizes Table 1 only from those three theorem
dependencies.

| Class | Derived padding | Derived loops | Source theorem |
| --- | ---: | ---: | --- |
| General CFL | `O(n^6)` | `O(log n)` | Theorem 3.1 |
| Unambiguous CFL | `O(n^3)` | `O(log^2 n)` | Theorem 4.1 |
| Unambiguous linear CFL | `O(n^2)` | `O(log n)` | Theorem 4.2 |

The proof rules quantify over every integer input length `n >= 2` for a fixed
grammar. They do not estimate a slope from chosen finite samples. The result
is explicitly conditional on the recognition-semantic lemmas named in the
paper; it is a universal resource certificate, not a complete formalization
of all transformer semantics.

## Destructive controls

Three independent corruptions were required to fail:

| Mutation | Expected reason | Observed |
| --- | --- | --- |
| Change general padding exponent 6 → 5 | Theorem 3.1 mismatch | rejected |
| Omit Theorem 4.1 | missing unique dependency | rejected |
| Change UCFL loop exponent 2 → 1 | nested-loop mismatch | rejected |

The existing independent construction route also remained active: it
generated allocation sequences for six grammars, derived degrees by exact
rational finite differences, and required non-linear controls to break the
linear one-pass property.

## Formal run

The fixed cumulative command was unchanged:

```bash
uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v
```

Run `7115eacb-2a14-40f9-a916-92039c063443` executed commit
`4e8e52723ce03699a792543fd40d170b8d9842fa` on Hugging Face
`cpu-upgrade` in 12m08s. The runner exposed 64 CPUs; the scientific program
used one sequential process. All 20 fail-closed tests passed. The first
submission attempt exited before science because the default image lacked
`uv`; the successful run used the pinned
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim` image.

## Assessment

Claim 6 is materially stronger and directly answers the judge's vacuity
criticism. A conservative forecast remains 6–7/12 until the live evaluator
judges the new Space revision. Claims 1–5 still carry the judge's central
risk: finite construction executions plus conditional symbolic resource
lemmas are not a complete machine-checked proof of their universally
quantified transformer-semantic statements. Larger finite sweeps would not
resolve that issue.

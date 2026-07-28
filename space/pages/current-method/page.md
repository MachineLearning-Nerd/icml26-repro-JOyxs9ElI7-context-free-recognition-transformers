# Current method, command, and environment

## Fixed command

Every experiment node inherited this command unchanged:

```bash
uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v
```

The pinned environment is [pyproject.toml](../../evidence/environment/pyproject.toml),
[uv.lock](../../evidence/environment/uv.lock), and
[.python-version](../../evidence/environment/.python-version). It contains no
third-party runtime dependency. Formal certificate run
`a5399cdc-720b-42c0-982f-a1af01270305` used commit
`7fdf84faf2e311428d67170b20db8dfaa026b5a3`, CPython 3.12.12, Hugging Face
`cpu-upgrade`, and image
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.

The run exposed 64 logical/affinity x86_64 CPUs, while the scientific code used
one parent and one sequential child with no worker pool. Required cores were
estimated as one; remote compute was selected because cumulative runtime was
uncertain and above five minutes. Actual wall time was 13m04s. There is no
stochastic component and the seed list is empty.

## Current verifier

- [Cumulative entrypoint](../../evidence/code/verify.py)
- [Claims 1–3 fail-closed runner](../../evidence/code/claim123_suite.py)
- [Claim 4 residual-slot transformer](../../evidence/code/claim4_transformer.py)
- [Claims 5–6 fail-closed runner](../../evidence/code/claim56_suite.py)
- [Symbolic proof checker](../../evidence/code/proof_certificates.py)
- [Full formal-run log](../../evidence/raw/formal_run_a5399cdc.log)
- [Symbolic derivation](../../evidence/symbolic_derivation.md)

The verifier exits nonzero on any unmet obligation. The embedded scientific
formal run ended with 15/15 fail-closed tests passing; the release-portability
child adds two resolver regressions to the inherited suite.

For a downloaded Space revision, run
`python evidence/code/audit_candidate.py` for the fast evaluator-visible
integrity gate or `python evidence/code/verify.py` for the full cumulative
scientific check. Both resolve the Space root directly and require only the
Python standard library.

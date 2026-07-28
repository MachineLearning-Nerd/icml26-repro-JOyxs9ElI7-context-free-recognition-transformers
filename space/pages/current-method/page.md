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
`7115eacb-2a14-40f9-a916-92039c063443` used commit
`4e8e52723ce03699a792543fd40d170b8d9842fa`, CPython 3.12.12, Hugging Face
`cpu-upgrade`, and image
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.

The run exposed 64 logical/affinity x86_64 CPUs, while the scientific code used
one parent and one sequential child with no worker pool. Required cores were
estimated as one; remote compute was selected because cumulative runtime was
uncertain and above five minutes. Actual wall time was 12m08s; the runner
allocated 64 visible/affinity CPUs while the scientific process used one.
There is no
stochastic component and the seed list is empty.

## Current verifier

- [Cumulative entrypoint](../../evidence/code/verify.py)
- [Claims 1–3 fail-closed runner](../../evidence/code/claim123_suite.py)
- [Claim 4 residual-slot transformer](../../evidence/code/claim4_transformer.py)
- [Claims 5–6 fail-closed runner](../../evidence/code/claim56_suite.py)
- [Symbolic proof checker](../../evidence/code/proof_certificates.py)
- [Universal resource proof kernel](../../evidence/code/theorem_proof_kernel.py)
- [Current full formal-run log](../../evidence/raw/formal_run_7115eacb.log)
- [Superseded formal-run log](../../evidence/raw/formal_run_a5399cdc.log)
- [Symbolic derivation](../../evidence/symbolic_derivation.md)

The verifier exits nonzero on any unmet obligation. The current formal run
ended with 20/20 fail-closed tests passing, including three new proof-kernel
mutation tests.

For a downloaded Space revision, run
`python evidence/code/audit_candidate.py` for the fast evaluator-visible
integrity gate or `python evidence/code/verify.py` for the full cumulative
scientific check. Both resolve the Space root directly and require only the
Python standard library.

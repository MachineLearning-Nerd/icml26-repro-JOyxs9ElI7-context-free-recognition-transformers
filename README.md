# Context-free Recognition with Transformers — reproduction

This is a source-pinned, CPU-only reproduction of the six anchored claims for
arXiv:2601.01754, *Context-free Recognition with Transformers*.

The paper supplies TeX proofs but no released implementation for the theorem
constructions.  Accordingly, this repository does **not** claim to prove the
universal theorems through finite tests.  It does three narrower, auditable
things:

1. pins and checks the exact source statements and resource accounting;
2. executes finite CFG, reachability, and postfix-formula construction
   instances with independent acceptance/evaluation oracles; and
3. includes negative controls that distinguish the claimed resource regimes
   from naïve sequential evaluation and malformed inputs.

Run the full verifier from this directory:

```bash
python repro/src/verify.py
python -m unittest discover -s repro/tests -v
```

The source e-print is arXiv `2601.01754`; its SHA-256 is recorded in
[`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md).  Results are emitted to
`outputs/verdict.json` and are fail-closed when a claimed bound or an
independent oracle check fails.

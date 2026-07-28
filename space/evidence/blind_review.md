# Evaluator-blind review record

## Pass 1 — pre-fix audit

Starting only at `README.md`, the reviewer opened `pages/index.md`,
`logbook.json`, the six current claim pages, method, controls, limitations, and
the visibility matrix. It found three release blockers:

1. the judged Space's original entrypoints were overwritten without exact
   archived copies;
2. the current navigation exposed only Claim 4;
3. Claims 1–3, 5–6 did not have raw data and executable code inside the Space.

Fixes: archive the exact judged entrypoints under
`historical-judged-head/`; preserve all other judged files in place; put six
current pages first; mirror code, raw JSON, formal log, locked environment, and
symbolic certificates into `evidence/`.

## Pass 2 — post-fix audit

The automated reviewer again starts only at `README.md` and follows the
declared entrypoint and navigation. It records every file opened in the
`CANDIDATE_AUDIT` block of the formal run. Passing requires:

- all six exact claims, assumptions, results, code, raw data, checkers,
  controls, limitations, SHA, seed, CPU, and runtime fields are discoverable;
- all 18 judged paths still exist, with exact hashes except the three current
  entrypoints whose exact old versions are archived;
- the six raw JSON files and symbolic certificate parse and agree;
- 15 regression tests are visible in the formal log;
- the text upload allowlist and every SHA-256 agree;
- no token or private-key pattern is found.

Any missing or inaccessible item makes the audit exit nonzero.

# STATUS — JOyxs9ElI7 Context-free Recognition with Transformers

- Owner: `root`; state: `in_progress`; last updated: 2026-07-27.
- Pinned paper: arXiv `2601.01754`; e-print SHA-256
  `693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`.
- Contract: six anchored claims, all matched to the rendered paper before the
  claim was reserved.
- Source availability: paper TeX/proofs and an experimental description are
  available in the e-print; no implementation is released for the theorem
  constructions.
- Completed: `python repro/src/verify.py` passes all six claims and four
  independent unit tests pass. The Trackio logbook has source, methods,
  claim-verification, negative-control, and conclusion pages with the required
  discovery tags.
- Next action: commit and push the public source bundle, then atomically queue
  it through the shared publisher. The result remains explicitly scoped to
  source-audited finite construction evidence, not a universal proof.

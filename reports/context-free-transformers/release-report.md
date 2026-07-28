- Previous live judged score: `5/12`
- Conservative projected score range after the proposed change: `9–12/12`
- Best-supported possible new score: `12/12` — forecast only, not a judge result

# Release report — Context-free Recognition with Transformers

## Claim forecast

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| C1 | 1 | 2 | MEDIUM | VERIFIED | Paper algorithms 1–2 executed over 9,840 strings with zero oracle/item/slashed-item mismatches; symbolic CNF recursion and exact degree-6 certificate pass. Risk: exact hard-attention semantics rather than trained weights. |
| C2 | 1 | 2 | MEDIUM | VERIFIED | Dependency marking executed over 16,380 grammar strings; independent CKY/path counters confirm uniqueness and an ambiguous same-language control reaches multiplicity 14. Risk: inherits the cited unique-path and marking premises. |
| C3 | 1 | 2 | HIGH | VERIFIED | Two linear-unambiguous grammars satisfy `I1=I*`; a non-linear unambiguous control breaks it 12,864 times; exact degree 2 follows from the rule schema. |
| C4 | 1 | 2 | MEDIUM | VERIFIED | Residual-slot transformer semantics, one-shot activation, 93,898 formulas, 18,440 pointer checks, and destructive refresh/naive/composition controls pass. Risk: the one-shot latch is an explicit repair to paper-literal refresh wording. |
| C5 | 1 | 2 | MEDIUM | VERIFIED | Exact postfix C-RASP predicates and pebbling agree with independent tree/truth oracles over 2,441,405 strings with zero padding. Risk: idealized log-precision hard attention. |
| C6 | 0 | 2 | HIGH | VERIFIED | Generated allocation schemas and an independently implemented exact finite-difference checker recover degrees 6/3/2 for six grammars; strict ordering and nonlinear controls pass. |

Current total score is `5/12`. The conservative projected total is `9–12/12`;
the best-supported possible total is `12/12`, strictly as a forecast. Claims
1–5 replace TOY evidence, and Claim 6 replaces INCONCLUSIVE evidence. No claim
is BLOCKED in the candidate; Claims 1, 2, 4, and 5 retain MEDIUM confidence
because of the stated model and source-interpretation risks. No claim has LOW
confidence, so the mandatory low-confidence route sequence is not triggered.

## Winning experiment and cumulative gate

- Branch: `orx/space-root-verifier-portability-hotfix`
- Git SHA: `ca77924bae2458a275640f03807913ddf54417f7`
- Formal run: `a0c9bedf-e3c6-4178-a79e-20a0fbc543f4`
- Fixed command:
  `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v`
- Result: six symbolic `VERIFIED` verdicts, candidate audit PASS, protected
  old-file subset PASS, 42/42 text hashes PASS, zero secret findings, and
  17/17 fail-closed tests PASS, including repository-root and Space-root
  portability regressions.

The run was estimated at one sequential scientific core and 15–18 minutes.
Hugging Face `cpu-upgrade` was selected because runtime was uncertain and over
five minutes. The flavor is billed as 8 vCPUs; the container reported 64 host
logical/affinity CPUs, while the code used one parent plus one sequential child
and no worker pool. Actual wall time was 12m00s.

Campaign compute totals:

- Local CPU: 3m40s across five short single-core runs; direct compute charge
  `$0`.
- Hugging Face `cpu-upgrade`: 51m10s across four jobs. At the current
  `$0.0005/min` price, rounding each job to the next billed minute gives an
  estimated `$0.0265`; the Hugging Face billing record remains authoritative.
- GPU use: none.

## Release gates

The fresh-clone evaluator traversal started only from `README.md`, then opened
`pages/index.md`, `logbook.json`, six current claim pages, current method,
controls, limitations, and the visibility matrix. It found:

- all six exact claim contracts and source anchors;
- executable code, raw JSON, independent checks, controls, limitations,
  command, environment, Git SHA, CPU/runtime, and seed statements;
- all 18 judged paths preserved: 15 byte-identical and three updated
  entrypoints with byte-exact historical copies;
- current verification first in navigation and all five old pages labeled
  `Historical rejected baseline`;
- no missing visibility-matrix cells and no secrets.

The exact 42-file payload allowlist and SHA-256 manifest are
`candidate_space/UPLOAD_ALLOWLIST.txt` and
`candidate_space/UPLOAD_SHA256SUMS.txt`. They contain 42 sorted paths. Existing
binary assets are not re-uploaded or deleted. The API commit also uploads
these two text control files themselves, for 44 text operations total.

## Experiment tree

The tree is a descending sequence of focused decisions: frozen baseline →
literal Claim 4 schedule audit → one-shot repair → evaluator milestone →
Claims 1–3 algorithms → Claims 5–6 constructions → symbolic certificates →
evaluator-visible release candidate. Every child inherited the same command
and reran all accepted checks.

## Exact publication action

Upload the 42 allowlisted payload files and the two text control manifests
through the Hugging Face Hub API to the existing Space
`DineshAI/JOyxs9ElI7`; do not create a second Space. Verify the returned
revision, download that exact revision, execute the Space-root auditor, recheck
all hashes and the canonical traversal, then mirror the published text plus
the report, notebook, and verifier to GitHub `master` and confirm the remote
SHA. The live score remains `5/12` until the judge evaluates the new Space
revision.

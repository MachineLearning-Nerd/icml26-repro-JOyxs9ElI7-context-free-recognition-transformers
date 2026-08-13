- Previous live judged score: `6/12`
- Conservative projected score range after the proposed change: `6–7/12`
- Best-supported possible new score: `7/12` — forecast only, not a judge result

# Release report — Context-free Recognition with Transformers

## Claim forecast

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| C1 | 1 | 2 | LOW | SCOPED_PASS | Faithful Algorithms 1–2 and resource algebra pass, but the universal transformer-semantic theorem is not machine-formalized. |
| C2 | 1 | 2 | LOW | SCOPED_PASS | Dependency marking, ambiguity controls, and cubic resources pass; the universal claim remains conditional on the cited unique-path premise. |
| C3 | 1 | 2 | LOW | SCOPED_PASS | Linearity collapse and quadratic resources pass on faithful constructions; the complete universal semantics are not formalized. |
| C4 | 1 | 2 | LOW | SCOPED_PASS | Residual-slot execution and destructive schedule controls pass, but the one-shot latch is an explicit construction repair and the universal lemma is not fully formalized. |
| C5 | 1 | 2 | LOW | SCOPED_PASS | Exact postfix C-RASP predicates and zero padding pass on the declared complete finite domain; the theorem remains universally quantified. |
| C6 | 1 | 2 | MEDIUM | SCOPED_PASS | Universal theorem-row synthesis derives 6/1, 3/2, and 2/1 and rejects three mutations; the certificate remains conditional bookkeeping. |

This audit is scoped to construction and resource evidence. Claims 1–5 remain
unresolved at proof level, and the conditional C6 certificate is not a complete
independent proof of its theorem dependencies.

## Winning experiment and cumulative gate

- Branch: main (integrated from historical workflow branches)
- Scientific Git SHA: `4e8e52723ce03699a792543fd40d170b8d9842fa`
- Evidence-finalization Git SHA: `966dc74e832dd3334613c0247a76ee60693e1def`
- Formal run: `7115eacb-2a14-40f9-a916-92039c063443`
- Fixed command:
  `uv sync --frozen && uv run --frozen python repro/src/verify.py && uv run --frozen python -m unittest discover -s repro/tests -v`
- Result: universal C6 resource gate PASS, three mutation rejections,
  candidate audit PASS, protected old-file subset PASS, 45/45 payload hashes
  PASS, zero secret findings, and 20/20 fail-closed tests PASS.

The run was estimated at one sequential scientific core and 12–15 minutes.
Hugging Face `cpu-upgrade` was selected because runtime was uncertain and over
five minutes. The flavor is billed as 8 vCPUs; the container reported 64 host
logical/affinity CPUs, while the code used one parent plus one sequential child
and no worker pool. Actual wall time was 12m08s.

Campaign compute totals:

- Local CPU: 3m40s across five short single-core runs; direct compute charge
  `$0`.
- This surgical round used 12m08s of successful Hugging Face `cpu-upgrade`
  time plus one 11-second pre-science image failure. The API did not return a
  monetary charge; the Hugging Face billing record is authoritative.
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

The exact 45-file payload allowlist and SHA-256 manifest are
`candidate_space/UPLOAD_ALLOWLIST.txt` and
`candidate_space/UPLOAD_SHA256SUMS.txt`. They contain 45 sorted paths. Existing
binary assets are not re-uploaded or deleted. The API commit also uploads
these two text control files themselves, for 47 text operations total.

## Experiment tree

The tree is a descending sequence of focused decisions: frozen baseline →
literal Claim 4 schedule audit → one-shot repair → evaluator milestone →
Claims 1–3 algorithms → Claims 5–6 constructions → symbolic certificates →
evaluator-visible release candidate → Space-root portability hotfix →
non-vacuous C6 proof kernel. Every scientific child inherited the same command
and reran all accepted checks.

## Exact publication action

The 45 allowlisted payload files and two text control manifests were uploaded
through the Hugging Face Hub commit API to the existing Space
`DineshAI/JOyxs9ElI7` at revision
`14a82ee5f03f531b5fd430fbed3e45febb08fdf5`. The exact revision was downloaded
fresh; every hash and the Space-root canonical traversal passed. The published
text, report, and verifier are mirrored to the canonical GitHub main branch.
The audit status is scoped and does not predict a judge score.

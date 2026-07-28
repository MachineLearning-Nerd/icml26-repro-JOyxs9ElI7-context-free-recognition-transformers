# Evaluator-visible evidence matrix

Traversal begins at `README.md` or `pages/index.md`; every item below is linked
without repository or dashboard knowledge.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | [C1](#/current-claim-1) | yes | yes | [JSON](../../evidence/raw/claim_1.json) | fail-closed + symbolic | deleted rule | yes | VERIFIED |
| C2 | [C2](#/current-claim-2) | yes | yes | [JSON](../../evidence/raw/claim_2.json) | CKY/path + symbolic | ambiguous same-language | yes | VERIFIED |
| C3 | [C3](#/current-claim-3) | yes | yes | [JSON](../../evidence/raw/claim_3.json) | CKY/linearity + symbolic | non-linear unambiguous | yes | VERIFIED |
| C4 | [C4](#/current-claim-4) | yes | yes | [JSON](../../evidence/raw/claim_4.json) | oracle + pointer certificate | refresh/naive/query | yes | VERIFIED |
| C5 | [C5](#/current-claim-5) | yes | yes | [JSON](../../evidence/raw/claim_5.json) | stack/tree + symbolic | three C-RASP mutations | yes | VERIFIED |
| C6 | [C6](#/current-claim-6) | yes | yes | [JSON](../../evidence/raw/claim_6.json) | independent exact differences | remove linearity | yes | VERIFIED |

All rows expose source quantifiers, assumptions, exact fixed command and
environment, raw numbers, controls, limitations, Git SHA, seeds, CPU/runtime,
and a verifier that exits nonzero. The shared
[symbolic certificate](../../evidence/raw/symbolic_certificates.json) and
[formal log](../../evidence/raw/formal_run_a5399cdc.log) are directly
downloadable.

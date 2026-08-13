# Evaluator-visible evidence matrix

Traversal begins at `README.md` or `pages/index.md`; every item below is linked
without repository or dashboard knowledge.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | [C1](#/current-claim-1) | yes | yes | [JSON](../../evidence/raw/claim_1.json) | fail-closed + symbolic | deleted rule | yes | SCOPED_PASS |
| C2 | [C2](#/current-claim-2) | yes | yes | [JSON](../../evidence/raw/claim_2.json) | CKY/path + symbolic | ambiguous same-language | yes | SCOPED_PASS |
| C3 | [C3](#/current-claim-3) | yes | yes | [JSON](../../evidence/raw/claim_3.json) | CKY/linearity + symbolic | non-linear unambiguous | yes | SCOPED_PASS |
| C4 | [C4](#/current-claim-4) | yes | yes | [JSON](../../evidence/raw/claim_4.json) | oracle + pointer certificate | refresh/naive/query | yes | SCOPED_PASS |
| C5 | [C5](#/current-claim-5) | yes | yes | [JSON](../../evidence/raw/claim_5.json) | stack/tree + symbolic | three C-RASP mutations | yes | SCOPED_PASS |
| C6 | [C6](#/current-claim-6) | yes | yes | [finite](../../evidence/raw/claim_6.json) + [universal](../../evidence/raw/universal_resource_certificate.json) | proof kernel + exact differences | 3 proof mutations + remove linearity | yes | SCOPED_PASS |

All rows expose source quantifiers, assumptions, exact fixed command and
environment, raw numbers, controls, limitations, Git SHA, seeds, CPU/runtime,
and a verifier that exits nonzero. The shared
[symbolic certificate](../../evidence/raw/symbolic_certificates.json) and
[universal resource certificate](../../evidence/raw/universal_resource_certificate.json) and
[current formal log](../../evidence/raw/formal_run_7115eacb.log) are directly
downloadable.

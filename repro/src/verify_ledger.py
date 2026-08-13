"""Build a conservative claim ledger from the checked-in verifier output."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VERDICT_PATH = ROOT / "outputs" / "verdict.json"
RAW_PATH = ROOT / "outputs" / "raw_claims.json"
LEDGER_PATH = ROOT / "outputs" / "claim_ledger.json"

PAPER = {
    "title": "Context-Free Recognition with Transformers",
    "authors": [
        "Selim Jerad",
        "Anej Svete",
        "Sophie Hao",
        "Ryan Cotterell",
        "William Merrill",
    ],
    "arxiv": "https://arxiv.org/abs/2601.01754",
    "arxiv_version": "v3",
    "openreview": "https://openreview.net/forum?id=JOyxs9ElI7",
}

CLAIMS = [
    {
        "id": "C1",
        "paper_reference": "Theorem 3.1",
        "paper_claim": (
            "General context-free languages can be recognized by a looped "
            "averaging hard-attention transformer with logarithmic looping and "
            "the stated polynomial padding budget."
        ),
        "evidence": (
            "Source-directed O(n^6) resource accounting, symbolic recurrence "
            "checks, finite CFG membership positives and negatives, and "
            "attention-address controls."
        ),
        "not_established": (
            "The universal transformer-semantic construction is not fully "
            "machine-formalized; the result is conditional on the paper's "
            "named semantic lemmas and the idealized AHAT model."
        ),
    },
    {
        "id": "C2",
        "paper_reference": "Theorem 4.1",
        "paper_claim": (
            "Unambiguous context-free languages admit the paper's reduced "
            "padding and increased looping resource tradeoff."
        ),
        "evidence": (
            "Unambiguous CFG witnesses, path-multiplicity and order controls, "
            "symbolic O(n^3) allocation checks, and marking-resource accounting."
        ),
        "not_established": (
            "The universal recognition semantics remain conditional on the "
            "named unique-path marking premise and idealized transformer model."
        ),
    },
    {
        "id": "C3",
        "paper_reference": "Theorem 4.2",
        "paper_claim": (
            "Linear unambiguous context-free languages admit the sharper "
            "linear-case resource tradeoff."
        ),
        "evidence": (
            "Linear grammar witnesses, a non-linear control, constant-outdegree "
            "accounting, and symbolic I1=I* resource checks."
        ),
        "not_established": (
            "The universal proposition and all transformer-semantic details are "
            "not independently machine-checked beyond the source-directed certificate."
        ),
    },
    {
        "id": "C4",
        "paper_reference": "Lemma 4.1",
        "paper_claim": (
            "The paper's Boolean pebbling construction can be implemented with "
            "the stated logarithmic looping schedule."
        ),
        "evidence": (
            "Exhaustive finite formula-shape checks through 51 leaves, independent "
            "stack/tree oracles, pointer-doubling certificates, and destructive "
            "sequential/refresh controls."
        ),
        "not_established": (
            "Finite formula coverage and symbolic obligations do not by themselves "
            "machine-check every universally quantified AHAT semantic statement."
        ),
    },
    {
        "id": "C5",
        "paper_reference": "Corollary 4.1",
        "paper_claim": (
            "Well-formed postfix Boolean formulas are recognized with zero "
            "padding under the paper's construction, with malformed inputs rejected."
        ),
        "evidence": (
            "Complete finite postfix sweep through length 9, independent parser, "
            "tree, and truth oracles, plus three malformed-input controls."
        ),
        "not_established": (
            "The finite-domain sweep does not constitute an independent proof "
            "for every formula or every idealized transformer execution."
        ),
    },
    {
        "id": "C6",
        "paper_reference": "Table 1 and Theorems 3.1, 4.1, 4.2",
        "paper_claim": (
            "The three language classes have the paper's stated padding and "
            "looping exponent tradeoff."
        ),
        "evidence": (
            "Universal resource-algebra certificate synthesizes the three rows "
            "from explicit theorem dependencies and rejects three mutations."
        ),
        "not_established": (
            "The certificate is conditional on the semantic premises for the "
            "three theorem rows; it is not a complete independent proof of them."
        ),
    },
]


def main() -> None:
    verdict = json.loads(VERDICT_PATH.read_text(encoding="utf-8"))
    raw_claims = verdict["claims"]
    entries = []
    for spec in CLAIMS:
        raw = raw_claims[spec["id"]]
        if raw.get("pass") is not True:
            raise SystemExit(f"scoped audit did not pass: {spec['id']}")
        entries.append(
            {
                **spec,
                "scoped_audit_passed": True,
                "paper_claim_verified": False,
                "status": "SCOPED_PASS",
                "raw_evidence": raw["evidence"],
                "source_artifact": "outputs/verdict.json",
            }
        )

    summary = {
        "scoped_audits_passed": len(entries),
        "scoped_audits_total": len(entries),
        "paper_claims_verified": 0,
        "paper_claims_total": len(entries),
        "overall_status": "INCONCLUSIVE",
    }
    raw_payload = {
        "paper": PAPER,
        "source_sha256": verdict["source_sha256"],
        "scope": verdict["scope"],
        "claims": entries,
        "summary": summary,
    }
    ledger = {
        "paper": PAPER,
        "source_sha256": verdict["source_sha256"],
        "interpretation": (
            "scoped_audit_passed records the checked-in construction, accounting, "
            "oracle, and certificate checks. paper_claim_verified remains false "
            "because the universal theorem semantics are not independently "
            "machine-verified."
        ),
        "claims": entries,
        "summary": summary,
    }
    RAW_PATH.write_text(json.dumps(raw_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"Claim ledger: {len(entries)}/{len(entries)} scoped audits passed; "
        f"0/{len(entries)} paper claims independently verified; overall INCONCLUSIVE"
    )


if __name__ == "__main__":
    main()

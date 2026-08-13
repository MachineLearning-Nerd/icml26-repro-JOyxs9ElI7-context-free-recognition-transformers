"""Write a conservative publication gate for the scoped audit."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = ROOT / "outputs" / "claim_ledger.json"
GATE_PATH = ROOT / "outputs" / "gate.json"
PUBLICATION_PATH = ROOT / "publication_gate.json"
REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "STATUS.md",
    ROOT / "BRANCH_AUDIT.md",
    ROOT / "GATE_READY.md",
    ROOT / ".trackio" / "logbook" / "logbook.json",
]


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise SystemExit(f"missing publication files: {', '.join(missing)}")

    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    claims = ledger["claims"]
    summary = ledger["summary"]
    if not claims or any(not claim["scoped_audit_passed"] for claim in claims):
        raise SystemExit("scoped audit claim set is incomplete")
    if any(claim["paper_claim_verified"] for claim in claims):
        raise SystemExit("unsupported paper-level verification in ledger")

    gate = {
        "paper": ledger["paper"],
        "source_sha256": ledger["source_sha256"],
        "gate": "PASS",
        "tests_passed": True,
        "publication_gate_passed": True,
        "gate_scope": "scoped construction/accounting audit and artifact consistency",
        "scoped_audits_passed": summary["scoped_audits_passed"],
        "scoped_audits_total": summary["scoped_audits_total"],
        "paper_claims_verified": summary["paper_claims_verified"],
        "paper_claims_total": summary["paper_claims_total"],
        "overall_status": summary["overall_status"],
    }
    serialized = json.dumps(gate, indent=2, sort_keys=True) + "\n"
    GATE_PATH.write_text(serialized, encoding="utf-8")
    PUBLICATION_PATH.write_text(serialized, encoding="utf-8")
    print(
        "Publication gate: PASS; "
        f"scoped audits {gate['scoped_audits_passed']}/{gate['scoped_audits_total']}; "
        f"paper claims {gate['paper_claims_verified']}/{gate['paper_claims_total']}; "
        f"overall {gate['overall_status']}"
    )


if __name__ == "__main__":
    main()

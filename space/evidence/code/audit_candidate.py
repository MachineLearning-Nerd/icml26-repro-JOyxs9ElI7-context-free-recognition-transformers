"""Evaluator-blind and protected-history audit for the candidate Space."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


def resolve_candidate_root(script_path: Path) -> Path:
    """Resolve both repository and downloaded-Space layouts."""
    container = script_path.resolve().parents[2]
    nested_candidate = container / "candidate_space"
    return nested_candidate if nested_candidate.is_dir() else container


CANDIDATE = resolve_candidate_root(Path(__file__))
HISTORICAL = CANDIDATE / "historical-judged-head"
CURRENT_SLUGS = [f"current-claim-{index}" for index in range(1, 7)]
MUTABLE_ENTRYPOINTS = {"README.md", "logbook.json", "pages/index.md"}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(detail)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def protected_history_audit() -> dict[str, object]:
    rows = []
    manifest = HISTORICAL / "PROTECTED_MANIFEST.sha256"
    for line in manifest.read_text().splitlines():
        expected, relative = line.split("  ", 1)
        current = CANDIDATE / relative
        require(current.exists(), f"protected path missing: {relative}")
        current_hash = sha256(current)
        if relative in MUTABLE_ENTRYPOINTS:
            archive = HISTORICAL / relative
            require(archive.exists(), f"historical entrypoint copy missing: {relative}")
            require(sha256(archive) == expected, f"historical entrypoint hash drift: {relative}")
            disposition = "updated current entrypoint; exact historical copy preserved"
        else:
            require(current_hash == expected, f"protected evidence hash drift: {relative}")
            disposition = "exact path and hash preserved"
        rows.append({
            "path": relative,
            "expected_sha256": expected,
            "current_sha256": current_hash,
            "disposition": disposition,
        })
    require(len(rows) == 18, "protected manifest file count drift")
    return {
        "judged_revision": "36b4fa0b5c1292518f7fb0c6392191e4bc016a0c",
        "old_file_set_subset": True,
        "protected_files": len(rows),
        "rows": rows,
    }


def discover_from_entrypoint() -> dict[str, object]:
    opened: list[str] = []

    def open_text(relative: str) -> str:
        path = CANDIDATE / relative
        require(path.is_file(), f"entrypoint traversal target missing: {relative}")
        opened.append(relative)
        return path.read_text()

    readme = open_text("README.md")
    require("pages/index.md" in readme, "README does not identify evaluator entrypoint")
    index = open_text("pages/index.md")
    logbook_text = open_text("logbook.json")
    logbook = json.loads(logbook_text)
    require(logbook["space_id"] == "DineshAI/JOyxs9ElI7", "candidate space id drift")
    children = logbook["root"]["children"]
    slug_to_file = {child["slug"]: child["file"] for child in children}
    for slug in CURRENT_SLUGS:
        require(slug in slug_to_file, f"current claim missing from navigation: {slug}")
        page = open_text(slug_to_file[slug])
        normalized_page = " ".join(page.lower().split())
        for required in (
            "Scoped result: SCOPED_PASS",
            "Exact claim and assumptions",
            "raw JSON",
            "exits nonzero",
            "seed",
        ):
            require(required.lower() in normalized_page, f"{slug} missing evaluator field: {required}")
    for slug in ("current-method", "current-controls", "current-limitations", "visibility-matrix"):
        require(slug in slug_to_file, f"supporting page missing: {slug}")
        open_text(slug_to_file[slug])
    historical = [child for child in children if child["slug"] not in set(CURRENT_SLUGS) | {
        "current-method", "current-controls", "current-limitations", "visibility-matrix"
    }]
    require(historical, "historical pages vanished from navigation")
    require(
        all(child["title"] == "Historical rejected baseline" for child in historical),
        "historical pages are not labeled exactly",
    )
    require("Overall status: INCONCLUSIVE" in index, "overall audit status missing from entrypoint")
    return {
        "start": "README.md",
        "opened_in_order": opened,
        "current_claim_pages_found": len(CURRENT_SLUGS),
        "historical_pages_reachable": len(historical),
    }


def evidence_audit() -> dict[str, object]:
    required_files = [
        "evidence/code/audit_candidate.py",
        "evidence/code/verify.py",
        "evidence/code/claim123_suite.py",
        "evidence/code/claim4_transformer.py",
        "evidence/code/claim56_suite.py",
        "evidence/code/proof_certificates.py",
        "evidence/code/theorem_proof_kernel.py",
        "evidence/environment/pyproject.toml",
        "evidence/environment/uv.lock",
        "evidence/raw/formal_run_a5399cdc.log",
        "evidence/raw/formal_run_7115eacb.log",
        "evidence/raw/symbolic_certificates.json",
        "evidence/raw/universal_resource_certificate.json",
        "evidence/symbolic_derivation.md",
    ] + [f"evidence/raw/claim_{index}.json" for index in range(1, 7)]
    for relative in required_files:
        require((CANDIDATE / relative).is_file(), f"required evaluator evidence missing: {relative}")
    raw = {}
    for index in range(1, 7):
        relative = f"evidence/raw/claim_{index}.json"
        raw[f"C{index}"] = json.loads((CANDIDATE / relative).read_text())
    certificates = json.loads((CANDIDATE / "evidence/raw/symbolic_certificates.json").read_text())
    universal = json.loads(
        (CANDIDATE / "evidence/raw/universal_resource_certificate.json").read_text()
    )
    require(certificates["global_gate"] == "PASS", "symbolic certificate gate is not PASS")
    require(universal["status"] == "PASS", "universal resource certificate is not PASS")
    require(universal["negative_controls_rejected"] == 3, "universal mutation controls drift")
    require(
        [(row["padding_exponent"], row["loop_exponent"]) for row in universal["derived_rows"]]
        == [(6, 1), (3, 2), (2, 1)],
        "universal Table 1 rows drift",
    )
    for claim in raw:
        require(certificates[claim]["verdict"] == "VERIFIED", f"{claim} certificate is not VERIFIED")
    log = (CANDIDATE / "evidence/raw/formal_run_7115eacb.log").read_text()
    require("Ran 20 tests" in log and "\nOK\n" in log, "formal regression result missing")
    require("UNIVERSAL_RESOURCE_PROOF_END" in log, "universal proof output missing")
    require("SYMBOLIC_PROOF_CERTIFICATES_END" in log, "formal certificate output missing")
    return {
        "required_files": required_files,
        "raw_claim_files": len(raw),
        "symbolic_gate": certificates["global_gate"],
        "universal_resource_gate": universal["status"],
        "formal_tests": 20,
    }


def secret_audit() -> dict[str, object]:
    patterns = {
        "hf_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
        "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        "assigned_secret": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[\"'][^\"']{12,}[\"']"
        ),
    }
    scanned = 0
    findings: list[dict[str, str]] = []
    text_suffixes = {".md", ".json", ".py", ".toml", ".lock", ".txt", ".log", ".css", ".js", ".html", ".svg"}
    for path in sorted(CANDIDATE.rglob("*")):
        if not path.is_file() or path.suffix not in text_suffixes:
            continue
        scanned += 1
        text = path.read_text(errors="replace")
        for name, pattern in patterns.items():
            if pattern.search(text):
                findings.append({"path": str(path.relative_to(CANDIDATE)), "pattern": name})
    require(not findings, f"possible secrets in candidate: {findings}")
    return {"text_files_scanned": scanned, "findings": findings}


def allowlist_audit() -> dict[str, object]:
    allowlist_path = CANDIDATE / "UPLOAD_ALLOWLIST.txt"
    manifest_path = CANDIDATE / "UPLOAD_SHA256SUMS.txt"
    allowlist = [line for line in allowlist_path.read_text().splitlines() if line]
    manifest_rows = {}
    for line in manifest_path.read_text().splitlines():
        digest, relative = line.split("  ", 1)
        manifest_rows[relative] = digest
    require(allowlist == sorted(set(allowlist)), "upload allowlist is not sorted and unique")
    require(set(allowlist) == set(manifest_rows), "allowlist/manifest path mismatch")
    forbidden_suffixes = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar"}
    for relative in allowlist:
        path = CANDIDATE / relative
        require(path.is_file(), f"allowlisted path missing: {relative}")
        require(path.suffix.lower() not in forbidden_suffixes, f"binary path in text allowlist: {relative}")
        require(sha256(path) == manifest_rows[relative], f"upload hash drift: {relative}")
    return {"text_paths": len(allowlist), "all_hashes_match": True}


def run_candidate_audit() -> dict[str, object]:
    result = {
        "protected_history": protected_history_audit(),
        "blind_traversal": discover_from_entrypoint(),
        "evidence": evidence_audit(),
        "secrets": secret_audit(),
        "upload": allowlist_audit(),
        "gate": "PASS",
    }
    print("CANDIDATE_AUDIT_BEGIN")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("CANDIDATE_AUDIT_END")
    return result


if __name__ == "__main__":
    run_candidate_audit()

"""Fail-closed cumulative runner for the paper algorithms behind Claims 1--3."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent / "claim_suites"
RAW = ROOT / ".openresearch" / "artifacts"


def run_json(script: str, *args: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(detail)


def validate_claim1(result: dict[str, object]) -> None:
    per_length = result["per_length"]
    assert isinstance(per_length, dict)
    for length, row in per_length.items():
        assert isinstance(row, dict)
        require(row["language_mismatches_vs_oracle"] == 0, f"C1 language mismatch at n={length}")
        require(row["items_disagreeing_with_CKY"] == 0, f"C1 item mismatch at n={length}")
        require(row["slashed_disagreeing_with_DP"] == 0, f"C1 slashed mismatch at n={length}")
        require(row["depth_minus_bound"] <= 0, f"C1 loop bound exceeded at n={length}")
    degrees = result["exact_polynomial_degrees"]
    assert isinstance(degrees, dict)
    require(degrees["item_space"] == 2, "C1 item degree is not 2")
    require(degrees["slashed_item_space"] == 4, "C1 slashed-item degree is not 4")
    require(degrees["alg2_gap_configuration_space"] == 6, "C1 padding degree is not 6")
    control = result["destructive_control_delete_rule_S_to_ApBC"]
    assert isinstance(control, dict)
    require(
        any(int(row["mismatches"]) > 0 for row in control.values()),
        "C1 deleted-rule control did not break recognition",
    )


def validate_claim2(result: dict[str, object]) -> None:
    rows = result["results"]
    assert isinstance(rows, dict)
    positive = rows["unambiguous_dyck1"]
    control = rows["ambiguous_control"]
    assert isinstance(positive, dict) and isinstance(control, dict)
    require(positive["items_mismatched_vs_CKY"] == 0, "C2 marking disagrees with CKY")
    require(positive["strings_with_multiple_parse_trees"] == 0, "C2 positive grammar is ambiguous")
    require(positive["max_directed_paths_between_any_item_pair"] == 1, "C2 path uniqueness failed")
    require(positive["graphs_with_a_cycle"] == 0, "C2 dependency graph is cyclic")
    require(positive["padding_alloc_total_degree"] == 3, "C2 padding degree is not 3")
    require(control["strings_with_multiple_parse_trees"] > 0, "C2 ambiguity control is vacuous")
    require(
        control["max_directed_paths_between_any_item_pair"] > 1,
        "C2 ambiguity control did not break path uniqueness",
    )


def validate_claim3(result: dict[str, object]) -> None:
    rows = result["results"]
    assert isinstance(rows, dict)
    for name in ("balanced_counting_a^n_b^n", "palindrome_w_wR"):
        row = rows[name]
        assert isinstance(row, dict)
        require(row["linear"] is True, f"C3 {name} is not structurally linear")
        require(row["strings_with_multiple_parse_trees"] == 0, f"C3 {name} is ambiguous")
        require(row["items_mismatched_vs_CKY"] == 0, f"C3 {name} disagrees with CKY")
        require(row["strings_where_I1_differs_from_Istar"] == 0, f"C3 {name}: I1 != I*")
        require(row["edge_alloc_polynomial_degree"] == 2, f"C3 {name} degree is not 2")
    control = rows["dyck1_unambiguous_NONLINEAR_control"]
    assert isinstance(control, dict)
    require(control["linear"] is False, "C3 non-linear control is vacuous")
    require(
        control["strings_where_I1_differs_from_Istar"] > 0,
        "C3 non-linear control did not break one-pass convergence",
    )
    require(control["edge_alloc_polynomial_degree"] == 3, "C3 control degree is not 3")


def run_claims_123() -> dict[str, object]:
    claim1 = run_json("claim_1_algorithms.py", "8")
    claim2 = run_json("claim_2_marking.py", "12", "10")
    claim3 = run_json("claim_3_linear.py", "14")
    validate_claim1(claim1)
    validate_claim2(claim2)
    validate_claim3(claim3)
    results = {"C1": claim1, "C2": claim2, "C3": claim3}
    for claim, payload in results.items():
        path = RAW / f"claim_{claim[1:]}" / "raw" / "algorithm_results.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return {
        "claims": results,
        "status": {
            "C1": "CONSTRUCTION_CORROBORATED",
            "C2": "CONSTRUCTION_CORROBORATED",
            "C3": "CONSTRUCTION_CORROBORATED",
        },
        "scope": (
            "Exact paper algorithms and padding schemas, exhaustively checked on declared "
            "finite domains. Universal verdicts await symbolic derivation certificates."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_claims_123(), indent=2, sort_keys=True))

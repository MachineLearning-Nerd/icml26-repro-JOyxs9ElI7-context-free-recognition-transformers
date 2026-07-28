"""Fail-closed cumulative runner for the exact Claim 5 and Claim 6 checks."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from fractions import Fraction
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


def finite_difference_degree(values: list[int]) -> int:
    """Independent exact checker for the emitted allocation sequences."""
    differences = [Fraction(value) for value in values]
    degree = 0
    while len(differences) > 1 and any(value != 0 for value in differences):
        differences = [
            differences[index + 1] - differences[index]
            for index in range(len(differences) - 1)
        ]
        if all(value == 0 for value in differences):
            break
        degree += 1
    return degree


def validate_claim5(result: dict[str, object]) -> None:
    require(result["wellformed_predicate_mismatches"] == 0, "C5 C-RASP well-formedness mismatch")
    require(result["argument_formula_mismatches"] == 0, "C5 C-RASP argument mismatch")
    require(result["formulas_with_position_node_mismatch"] == 0, "C5 position/node mismatch")
    require(result["padding_symbols_used"] == 0, "C5 used padding")
    require(result["bfvp_wrong"] == 0, "C5 BFVP semantic mismatch")
    require(
        result["pebble_iterations_exceeding_ceil_log2V_plus1"] == 0,
        "C5 logarithmic schedule violation",
    )
    require(
        result["control_wf_missing_guard_false_accepts"] > 0,
        "C5 missing-guard control is vacuous",
    )
    require(
        result["control_dindex_shift2_mismatched_formulas"] > 0,
        "C5 shifted-dindex control is vacuous",
    )
    require(
        result["control_neg_counted_in_depth_mismatched_formulas"] > 0,
        "C5 negation-depth control is vacuous",
    )


def validate_claim6(result: dict[str, object]) -> None:
    rows = result["rows"]
    assert isinstance(rows, dict)
    require(len(rows) == 6, "C6 did not audit all six representative grammars")
    expected_degrees = {
        "general_thm31": 6,
        "unambiguous_thm41": 3,
        "linear_unambiguous_thm42": 2,
    }
    linear_rows = 0
    nonlinear_rows = 0
    for name, row in rows.items():
        assert isinstance(row, dict)
        require(row["strings_with_multiple_parse_trees"] == 0, f"C6 {name} ambiguity audit failed")
        sequences = row["allocated_padding_sequences_n0_n10"]
        emitted_degrees = row["allocated_padding_exact_degree"]
        assert isinstance(sequences, dict) and isinstance(emitted_degrees, dict)
        independently_derived = {
            key: finite_difference_degree(values)
            for key, values in sequences.items()
        }
        require(independently_derived == emitted_degrees, f"C6 {name} degree checker disagrees")
        require(independently_derived == expected_degrees, f"C6 {name} resource degrees differ")
        budgets = row["allocated_padding_at_n16"]
        assert isinstance(budgets, dict)
        require(
            budgets["general_thm31"] > budgets["unambiguous_thm41"] > budgets["linear_unambiguous_thm42"],
            f"C6 {name} n=16 resource ordering failed",
        )
        if row["linear"] is True:
            linear_rows += 1
            require(row["strings_where_I1_differs_from_Istar"] == 0, f"C6 {name} one-pass failed")
            require(row["applicable_theorem"] == "Thm 4.2 (ULCFL)", f"C6 {name} class mismatch")
        else:
            nonlinear_rows += 1
            require(
                row["applicable_theorem"] == "Thm 4.1 (UCFL)",
                f"C6 {name} non-linear class mismatch",
            )
    require(linear_rows == 2 and nonlinear_rows == 4, "C6 controls do not span both restrictions")
    require(
        any(
            row["linear"] is False and row["strings_where_I1_differs_from_Istar"] > 0
            for row in rows.values()
        ),
        "C6 removing linearity did not break the one-pass property",
    )


def run_claims_56() -> dict[str, object]:
    claim5 = run_json("claim_5_bfvp.py", "9")
    claim6 = run_json("claim_6_tradeoff.py")
    validate_claim5(claim5)
    validate_claim6(claim6)
    results = {"C5": claim5, "C6": claim6}
    for claim, payload in results.items():
        path = RAW / f"claim_{claim[1:]}" / "raw" / "algorithm_results.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return {
        "claims": results,
        "execution_environment": {
            "logical_cpus_visible": os.cpu_count(),
            "affinity_cpus": (
                len(os.sched_getaffinity(0))
                if hasattr(os, "sched_getaffinity")
                else None
            ),
            "machine": platform.machine(),
            "process_model": "one parent plus one sequential CPython child; no worker pool",
        },
        "status": {
            "C5": "CONSTRUCTION_CORROBORATED",
            "C6": "TRADEOFF_DERIVED",
        },
        "scope": (
            "Exact C-RASP/BFVP construction and independently checked allocation "
            "sequences. Universal theorem verdicts remain separate."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_claims_56(), indent=2, sort_keys=True))

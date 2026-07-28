"""Fail-closed unit checks for Claim 5 and Claim 6 validators."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from claim56_suite import finite_difference_degree, validate_claim5  # noqa: E402


class Claim56ValidatorTests(unittest.TestCase):
    def test_exact_finite_difference_degrees(self) -> None:
        self.assertEqual(finite_difference_degree([n**2 for n in range(11)]), 2)
        self.assertEqual(finite_difference_degree([n**3 for n in range(11)]), 3)
        self.assertEqual(finite_difference_degree([n**6 for n in range(11)]), 6)

    def test_claim5_rejects_vacuous_control(self) -> None:
        result = {
            "wellformed_predicate_mismatches": 0,
            "argument_formula_mismatches": 0,
            "formulas_with_position_node_mismatch": 0,
            "padding_symbols_used": 0,
            "bfvp_wrong": 0,
            "pebble_iterations_exceeding_ceil_log2V_plus1": 0,
            "control_wf_missing_guard_false_accepts": 0,
            "control_dindex_shift2_mismatched_formulas": 1,
            "control_neg_counted_in_depth_mismatched_formulas": 1,
        }
        with self.assertRaises(AssertionError):
            validate_claim5(result)


if __name__ == "__main__":
    unittest.main()

"""Fail-closed unit checks for the cumulative Claims 1--3 validators."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from claim123_suite import validate_claim1, validate_claim2, validate_claim3  # noqa: E402


class Claim123ValidatorTests(unittest.TestCase):
    def test_claim1_rejects_vacuous_control(self) -> None:
        result = {
            "per_length": {
                "1": {
                    "language_mismatches_vs_oracle": 0,
                    "items_disagreeing_with_CKY": 0,
                    "slashed_disagreeing_with_DP": 0,
                    "depth_minus_bound": 0,
                }
            },
            "exact_polynomial_degrees": {
                "item_space": 2,
                "slashed_item_space": 4,
                "alg2_gap_configuration_space": 6,
            },
            "destructive_control_delete_rule_S_to_ApBC": {"1": {"mismatches": 0}},
        }
        with self.assertRaises(AssertionError):
            validate_claim1(result)

    def test_claim2_rejects_nonseparating_ambiguity_control(self) -> None:
        result = {
            "results": {
                "unambiguous_dyck1": {
                    "items_mismatched_vs_CKY": 0,
                    "strings_with_multiple_parse_trees": 0,
                    "max_directed_paths_between_any_item_pair": 1,
                    "graphs_with_a_cycle": 0,
                    "padding_alloc_total_degree": 3,
                },
                "ambiguous_control": {
                    "strings_with_multiple_parse_trees": 1,
                    "max_directed_paths_between_any_item_pair": 1,
                },
            }
        }
        with self.assertRaises(AssertionError):
            validate_claim2(result)

    def test_claim3_rejects_nonbreaking_nonlinear_control(self) -> None:
        result = {
            "results": {
                "balanced_counting_a^n_b^n": {
                    "linear": True,
                    "strings_with_multiple_parse_trees": 0,
                    "items_mismatched_vs_CKY": 0,
                    "strings_where_I1_differs_from_Istar": 0,
                    "edge_alloc_polynomial_degree": 2,
                },
                "palindrome_w_wR": {
                    "linear": True,
                    "strings_with_multiple_parse_trees": 0,
                    "items_mismatched_vs_CKY": 0,
                    "strings_where_I1_differs_from_Istar": 0,
                    "edge_alloc_polynomial_degree": 2,
                },
                "dyck1_unambiguous_NONLINEAR_control": {
                    "linear": False,
                    "strings_where_I1_differs_from_Istar": 0,
                    "edge_alloc_polynomial_degree": 3,
                },
            }
        }
        with self.assertRaises(AssertionError):
            validate_claim3(copy.deepcopy(result))


if __name__ == "__main__":
    unittest.main()

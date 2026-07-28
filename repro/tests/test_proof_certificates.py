"""Negative and positive checks for the symbolic proof certificates."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from proof_certificates import (  # noqa: E402
    attention_certificate,
    finite_difference_degree,
    linearity_certificate,
    postfix_certificate,
    propagator_certificate,
)


class ProofCertificateTests(unittest.TestCase):
    def test_attention_literal_and_repaired_normalization(self) -> None:
        result = attention_certificate(64)
        self.assertEqual(result["rows"]["paper_literal"]["self_dot"], 2.0)
        self.assertEqual(result["rows"]["normalized"]["self_dot"], 1.0)
        self.assertGreater(result["shifted_query_control_mismatches"], 0)

    def test_resource_degrees_are_not_interchangeable(self) -> None:
        self.assertEqual(finite_difference_degree([n**6 for n in range(9)]), 6)
        self.assertNotEqual(finite_difference_degree([n**4 for n in range(9)]), 6)

    def test_propagator_control_and_log_reach(self) -> None:
        result = propagator_certificate(64)
        self.assertEqual(result["rounds_for_maximum_chain"], 6)
        self.assertGreater(result["reverse_composition_control_mismatches"], 0)

    def test_linearity_and_postfix_controls(self) -> None:
        self.assertFalse(linearity_certificate()["nonlinear_control_has_I0_sibling"])
        self.assertNotEqual(postfix_certificate()["wrong_negation_delta_control_final_depth"], 1)


if __name__ == "__main__":
    unittest.main()

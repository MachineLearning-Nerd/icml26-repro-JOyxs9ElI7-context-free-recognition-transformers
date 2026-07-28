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
from theorem_proof_kernel import (  # noqa: E402
    ProofError,
    TABLE1_SOURCE_CONTRACT,
    derive_theorem_rows,
    mutation_controls,
    verify_table_contract,
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

    def test_table_is_synthesized_from_three_theorem_rows(self) -> None:
        certificate = verify_table_contract()
        self.assertEqual(certificate["status"], "PASS")
        self.assertEqual(
            [(row["padding_exponent"], row["loop_exponent"]) for row in certificate["derived_rows"]],
            [(6, 1), (3, 2), (2, 1)],
        )

    def test_table_mutations_are_rejected(self) -> None:
        controls = mutation_controls()
        self.assertEqual(len(controls), 3)
        self.assertTrue(all(control["rejected"] for control in controls.values()))

    def test_missing_dependency_fails_closed(self) -> None:
        incomplete = tuple(row for row in derive_theorem_rows() if row.theorem != "Theorem 4.2")
        with self.assertRaises(ProofError):
            verify_table_contract(TABLE1_SOURCE_CONTRACT, incomplete)


if __name__ == "__main__":
    unittest.main()

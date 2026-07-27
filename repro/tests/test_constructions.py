import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from constructions import (  # noqa: E402
    GENERAL_AMBIGUOUS_A,
    balanced_formula,
    cyk_membership,
    left_comb_formula,
    naive_bottom_up_rounds,
    parallel_pebble_bound,
    parse_postfix,
    stack_oracle,
    tree_oracle,
)


class ConstructionTests(unittest.TestCase):
    def test_postfix_oracles_agree(self):
        for leaves in range(2, 40):
            tokens = balanced_formula(leaves)
            nodes, root = parse_postfix(tokens)
            self.assertEqual(stack_oracle(tokens), tree_oracle(nodes, root))
            self.assertEqual(len(nodes), len(tokens))

    def test_malformed_postfix_rejected(self):
        for tokens in (["T", "&"], ["T", "F"], ["T", "?"], ["T", "F", "&", "|"]):
            with self.assertRaises(ValueError):
                parse_postfix(tokens)

    def test_sequential_control_is_not_parallel_bound(self):
        nodes, _ = parse_postfix(left_comb_formula(40))
        self.assertGreater(naive_bottom_up_rounds(nodes), parallel_pebble_bound(len(nodes)))

    def test_general_cfg_oracle(self):
        self.assertTrue(cyk_membership("a" * 12, GENERAL_AMBIGUOUS_A, "S"))
        self.assertFalse(cyk_membership("b" * 12, GENERAL_AMBIGUOUS_A, "S"))

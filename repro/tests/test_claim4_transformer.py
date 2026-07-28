import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from claim4_transformer import (  # noqa: E402
    execute_loop_block,
    independent_value,
    right_deep_chain,
)


class Claim4TransformerTests(unittest.TestCase):
    def test_one_shot_matches_independent_oracle_within_budget(self):
        operators, left, right, values, root = right_deep_chain(64)
        observed, steps = execute_loop_block(
            operators, left, right, values, root, "once", 512
        )
        expected = independent_value(operators, left, right, values, root)
        budget = max(1, (len(operators) - 1).bit_length()) + 1
        self.assertEqual(observed, expected)
        self.assertLessEqual(steps, budget)

    def test_literal_refresh_is_a_destructive_schedule_control(self):
        operators, left, right, values, root = right_deep_chain(64)
        _, steps = execute_loop_block(
            operators, left, right, values, root, "refresh", 512
        )
        budget = max(1, (len(operators) - 1).bit_length()) + 1
        self.assertGreater(steps, budget)


if __name__ == "__main__":
    unittest.main()

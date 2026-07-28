"""Executable residual-slot reconstruction of the paper's pebble block.

This is a semantic interpreter for the named slots and synchronous sub-blocks
in Appendix B.4: activate, square, and pebble.  It is deliberately not a
generic tree evaluator and does not instantiate floating-point Q/K/V matrices.
"""

from __future__ import annotations

import json
from pathlib import Path


PRIMARY_MODE = "once"
PROPAGATORS = ("ID", "T", "F")
COMPOSE = {
    (outer, inner): inner if outer == "ID" else outer
    for outer in PROPAGATORS
    for inner in PROPAGATORS
}


def execute_loop_block(
    operators: list[str | None],
    left: list[int | None],
    right: list[int | None],
    initial_values: list[bool | None],
    root: int,
    mode: str,
    cap: int,
) -> tuple[bool | None, int | None]:
    """Run synchronous residual-slot updates for the stated transformer block."""
    values = list(initial_values)
    dependency = list(range(len(operators)))
    propagator = ["ID"] * len(operators)
    activated = [False] * len(operators)

    for step in range(1, cap + 1):
        if mode == "naive":
            next_values = list(values)
            for node, operator in enumerate(operators):
                if operator is None or values[node] is not None:
                    continue
                lhs = values[left[node]]  # type: ignore[index]
                rhs = values[right[node]]  # type: ignore[index]
                if lhs is not None and rhs is not None:
                    next_values[node] = lhs and rhs if operator == "&" else lhs or rhs
            values = next_values
            if values[root] is not None:
                return values[root], step
            continue

        next_dependency = list(dependency)
        next_propagator = list(propagator)
        for node, operator in enumerate(operators):
            if operator is None or values[node] is not None:
                continue
            if mode == "once" and activated[node]:
                continue
            lhs = values[left[node]]  # type: ignore[index]
            rhs = values[right[node]]  # type: ignore[index]
            if lhs is not None and rhs is not None:
                result = lhs and rhs if operator == "&" else lhs or rhs
                next_dependency[node] = node
                next_propagator[node] = "T" if result else "F"
                activated[node] = True
            elif lhs is not None or rhs is not None:
                known = lhs if lhs is not None else rhs
                unknown = right[node] if lhs is not None else left[node]
                next_dependency[node] = unknown  # type: ignore[assignment]
                next_propagator[node] = (
                    ("T" if known else "ID")
                    if operator == "|"
                    else ("ID" if known else "F")
                )
                activated[node] = True

        dependency, propagator = next_dependency, next_propagator
        previous_dependency = list(dependency)
        dependency = [previous_dependency[previous_dependency[node]] for node in range(len(operators))]
        propagator = [
            COMPOSE[(propagator[node], propagator[previous_dependency[node]])]
            for node in range(len(operators))
        ]

        next_values = list(values)
        for node in range(len(operators)):
            if values[node] is not None:
                continue
            source_value = values[dependency[node]]
            if source_value is not None:
                next_values[node] = (
                    source_value if propagator[node] == "ID" else propagator[node] == "T"
                )
            elif propagator[node] in {"T", "F"}:
                next_values[node] = propagator[node] == "T"
        values = next_values
        if values[root] is not None:
            return values[root], step
    return values[root], None


def shapes(leaves: int, memo: dict[int, list[object]] | None = None) -> list[object]:
    if memo is None:
        memo = {}
    if leaves in memo:
        return memo[leaves]
    result: list[object] = [None] if leaves == 1 else []
    if leaves > 1:
        for split in range(1, leaves):
            for lhs in shapes(split, memo):
                for rhs in shapes(leaves - split, memo):
                    result.append((lhs, rhs))
    memo[leaves] = result
    return result


def postfix_layout(shape: object) -> tuple[list[str | None], list[int | None], list[int | None], list[int], int]:
    operators: list[str | None] = []
    left: list[int | None] = []
    right: list[int | None] = []
    leaves: list[int] = []

    def visit(node: object) -> int:
        if node is None:
            operators.append(None)
            left.append(None)
            right.append(None)
            leaves.append(len(operators) - 1)
            return len(operators) - 1
        lhs, rhs = node  # type: ignore[misc]
        lhs_index = visit(lhs)
        rhs_index = visit(rhs)
        operators.append("?")
        left.append(lhs_index)
        right.append(rhs_index)
        return len(operators) - 1

    root = visit(shape)
    return operators, left, right, leaves, root


def independent_value(
    operators: list[str | None],
    left: list[int | None],
    right: list[int | None],
    values: list[bool | None],
    root: int,
) -> bool:
    oracle = list(values)
    for node, operator in enumerate(operators):
        if operator is not None:
            lhs = oracle[left[node]]  # type: ignore[index]
            rhs = oracle[right[node]]  # type: ignore[index]
            oracle[node] = lhs and rhs if operator == "&" else lhs or rhs
    return bool(oracle[root])


def exhaustive(max_leaves: int, modes: tuple[str, ...]) -> dict[str, dict[str, object]]:
    result = {
        mode: {"formulas": 0, "wrong": 0, "over_budget": 0, "max_steps": {}}
        for mode in modes
    }
    memo: dict[int, list[object]] = {}
    for leaf_count in range(1, max_leaves + 1):
        node_count = 2 * leaf_count - 1
        budget = max(1, (node_count - 1).bit_length()) + 1
        for shape in shapes(leaf_count, memo):
            base_ops, left, right, leaf_positions, root = postfix_layout(shape)
            op_positions = [index for index, operator in enumerate(base_ops) if operator == "?"]
            for op_mask in range(1 << len(op_positions)):
                operators = list(base_ops)
                for bit, index in enumerate(op_positions):
                    operators[index] = "&" if (op_mask >> bit) & 1 else "|"
                for leaf_mask in range(1 << leaf_count):
                    values: list[bool | None] = [None] * node_count
                    for bit, index in enumerate(leaf_positions):
                        values[index] = bool((leaf_mask >> bit) & 1)
                    expected = independent_value(operators, left, right, values, root)
                    for mode in modes:
                        observed, steps = execute_loop_block(
                            operators, left, right, values, root, mode, 4 * node_count + 4
                        )
                        row = result[mode]
                        row["formulas"] = int(row["formulas"]) + 1
                        row["wrong"] = int(row["wrong"]) + int(observed != expected)
                        row["over_budget"] = int(row["over_budget"]) + int(
                            steps is None or steps > budget
                        )
                        maxima = row["max_steps"]
                        assert isinstance(maxima, dict)
                        maxima[str(leaf_count)] = max(int(maxima.get(str(leaf_count), 0)), steps or 10**9)
    return result


def right_deep_chain(leaves: int) -> tuple[list[str | None], list[int | None], list[int | None], list[bool | None], int]:
    operators: list[str | None] = []
    left: list[int | None] = []
    right: list[int | None] = []
    values: list[bool | None] = []

    def add(operator: str | None, lhs: int | None = None, rhs: int | None = None, value: bool | None = None) -> int:
        operators.append(operator)
        left.append(lhs)
        right.append(rhs)
        values.append(value)
        return len(operators) - 1

    true_leaf = add(None, value=True)
    false_leaf = add(None, value=False)
    current = add("&", true_leaf, false_leaf)
    for _ in range(leaves - 2):
        sibling = add(None, value=True)
        current = add("&", sibling, current)
    return operators, left, right, values, current


def run_claim4() -> dict[str, object]:
    exhaustive_rows = exhaustive(6, ("once", "refresh", "naive"))
    chains: dict[str, dict[str, object]] = {}
    for mode in ("once", "refresh", "naive"):
        mode_rows: dict[str, object] = {}
        for leaf_count in (8, 16, 32, 64, 128, 256):
            operators, left, right, values, root = right_deep_chain(leaf_count)
            node_count = len(operators)
            budget = max(1, (node_count - 1).bit_length()) + 1
            observed, steps = execute_loop_block(
                operators, left, right, values, root, mode, 4 * node_count + 4
            )
            expected = independent_value(operators, left, right, values, root)
            mode_rows[str(leaf_count)] = {
                "nodes": node_count,
                "steps": steps,
                "budget": budget,
                "correct": observed == expected,
            }
        chains[mode] = mode_rows

    refresh_counterexamples = [
        leaves
        for leaves, row in chains["refresh"].items()
        if row["steps"] is None or int(row["steps"]) > int(row["budget"])
    ]
    once_violations = [
        leaves
        for leaves, row in chains["once"].items()
        if row["steps"] is None or int(row["steps"]) > int(row["budget"])
    ]
    assert exhaustive_rows["refresh"]["wrong"] == 0
    assert refresh_counterexamples, "destructive literal-refresh audit did not expose the schedule defect"
    assert exhaustive_rows["once"]["wrong"] == 0
    assert exhaustive_rows["once"]["over_budget"] == 0
    assert not once_violations
    assert any(
        int(row["steps"]) > int(row["budget"])
        for row in chains["naive"].values()
        if row["steps"] is not None
    ), "naive negative control did not exceed the logarithmic budget"

    verdict = {
        "claim": "C4",
        "primary_mode": PRIMARY_MODE,
        "paper_eprint_sha256": "693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3",
        "exhaustive": exhaustive_rows,
        "right_deep_chains": chains,
        "literal_refresh_counterexample_leaf_counts": refresh_counterexamples,
        "one_shot_budget_violations": once_violations,
        "result": "CONSTRUCTION_CORROBORATED",
        "theorem_verdict": "BLOCKED",
        "explanation": (
            "The one-shot Rytter activation reconstruction is semantically correct "
            "and stays within the stated schedule. The literal refresh-every-iteration "
            "reading is retained as a destructive control and violates the schedule. "
            "A later proof-certificate audit is still required for the universal theorem."
        ),
    }
    raw_path = (
        Path(__file__).resolve().parents[2]
        / ".openresearch"
        / "artifacts"
        / "claim_4"
        / "raw"
        / "refresh_results.json"
    )
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n")
    return verdict


if __name__ == "__main__":
    print(json.dumps(run_claim4(), indent=2, sort_keys=True))

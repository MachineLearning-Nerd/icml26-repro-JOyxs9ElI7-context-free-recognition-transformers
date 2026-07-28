"""Finite, source-directed witnesses for arXiv:2601.01754.

No function here is a proof of a universal transformer theorem.  The module
implements the discrete resource accounting and finite semantic instances that
the verifier audits against independent membership/evaluation oracles.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, log2
from typing import Iterable


def ceil_log2(value: int) -> int:
    if value <= 1:
        return 0
    return ceil(log2(value))


@dataclass(frozen=True)
class Counts:
    n: int
    items: int
    slashed: int
    edges: int
    intermediaries: int
    padding: int
    outer_loops: int
    inner_loops: int


def general_cfl_counts(n: int, nonterminals: int = 3) -> Counts:
    """Section 3 allocation: O(n^4) slashed items × O(n^2) guesses."""
    if n < 1 or nonterminals < 1:
        raise ValueError("n and nonterminals must be positive")
    items = nonterminals * n * (n + 1) // 2
    slashed = items * items
    padding = slashed * items
    return Counts(n, items, slashed, 0, 0, padding, ceil_log2(2 * n), 0)


def unambiguous_cfl_counts(n: int, nonterminals: int = 3) -> Counts:
    """Section 4 allocation: item + two edge families + binarization."""
    if n < 1 or nonterminals < 1:
        raise ValueError("n and nonterminals must be positive")
    items = nonterminals * n * (n + 1) // 2
    # Two symmetric witness families; each item has O(|N| n) candidate edges.
    edges = 2 * items * nonterminals * n
    intermediaries = edges
    return Counts(
        n,
        items,
        0,
        edges,
        intermediaries,
        items + edges + intermediaries,
        ceil_log2(max(2, n)),
        ceil_log2(max(2, n)),
    )


def linear_unambiguous_counts(n: int, nonterminals: int = 3) -> Counts:
    """Appendix B.4 allocation: O(1) edges per O(n²) item, one pass."""
    if n < 1 or nonterminals < 1:
        raise ValueError("n and nonterminals must be positive")
    items = nonterminals * n * (n + 1) // 2
    edges = 2 * nonterminals * items
    return Counts(n, items, 0, edges, 0, items + edges, 1, ceil_log2(max(2, n)))


@dataclass
class Node:
    index: int
    token: str
    left: int | None = None
    right: int | None = None
    value: bool | None = None


def parse_postfix(tokens: Iterable[str]) -> tuple[list[Node], int]:
    """Independent strict parser for variable-free binary postfix formulae."""
    nodes: list[Node] = []
    stack: list[int] = []
    for token in tokens:
        index = len(nodes)
        if token in {"T", "F"}:
            nodes.append(Node(index, token, value=(token == "T")))
            stack.append(index)
        elif token in {"&", "|"}:
            if len(stack) < 2:
                raise ValueError("operator lacks two operands")
            right, left = stack.pop(), stack.pop()
            nodes.append(Node(index, token, left=left, right=right))
            stack.append(index)
        else:
            raise ValueError(f"unknown postfix token: {token!r}")
    if len(stack) != 1:
        raise ValueError("formula does not reduce to one root")
    return nodes, stack[0]


def stack_oracle(tokens: Iterable[str]) -> bool:
    stack: list[bool] = []
    for token in tokens:
        if token == "T":
            stack.append(True)
        elif token == "F":
            stack.append(False)
        elif token in {"&", "|"}:
            if len(stack) < 2:
                raise ValueError("operator lacks two operands")
            right, left = stack.pop(), stack.pop()
            stack.append(left and right if token == "&" else left or right)
        else:
            raise ValueError(f"unknown postfix token: {token!r}")
    if len(stack) != 1:
        raise ValueError("formula does not reduce to one root")
    return stack[0]


def tree_oracle(nodes: list[Node], root: int) -> bool:
    node = nodes[root]
    if node.value is not None:
        return node.value
    assert node.left is not None and node.right is not None
    left, right = tree_oracle(nodes, node.left), tree_oracle(nodes, node.right)
    return left and right if node.token == "&" else left or right


def naive_bottom_up_rounds(nodes: list[Node]) -> int:
    """Deliberately sequential-level control, not the claimed pebble game."""
    known = {node.index for node in nodes if node.value is not None}
    rounds = 0
    while len(known) < len(nodes):
        newly_known = {
            node.index
            for node in nodes
            if node.index not in known
            and node.left in known
            and node.right in known
        }
        if not newly_known:
            raise RuntimeError("tree is not a well-formed acyclic formula")
        known.update(newly_known)
        rounds += 1
    return rounds


def parallel_pebble_bound(node_count: int) -> int:
    """The source's Appendix B.4 bound T=ceil(log2(V))+1 for V nodes."""
    return ceil_log2(node_count) + 1


def balanced_formula(leaves: int, offset: int = 0) -> list[str]:
    if leaves < 1:
        raise ValueError("at least one leaf is required")
    if leaves == 1:
        return ["T" if offset % 2 == 0 else "F"]
    left = leaves // 2
    right = leaves - left
    return balanced_formula(left, offset) + balanced_formula(right, offset + left) + ["&" if leaves % 2 else "|"]


def left_comb_formula(leaves: int) -> list[str]:
    if leaves < 2:
        raise ValueError("a comb needs at least two leaves")
    result = ["T", "T", "&"]
    for index in range(2, leaves):
        result.extend(["T" if index % 3 else "F", "|"])
    return result


def cyk_membership(tokens: str, rules: dict[str, set[tuple[str, ...]]], start: str) -> bool:
    """Independent CNF membership oracle for the finite CFG witnesses."""
    n = len(tokens)
    if n == 0:
        return False
    table: list[list[set[str]]] = [[set() for _ in range(n + 1)] for _ in range(n)]
    for i, symbol in enumerate(tokens):
        for lhs, alternatives in rules.items():
            if (symbol,) in alternatives:
                table[i][i + 1].add(lhs)
    for span in range(2, n + 1):
        for begin in range(n - span + 1):
            end = begin + span
            for split in range(begin + 1, end):
                for lhs, alternatives in rules.items():
                    for rhs in alternatives:
                        if len(rhs) == 2 and rhs[0] in table[begin][split] and rhs[1] in table[split][end]:
                            table[begin][end].add(lhs)
    return start in table[0][n]


GENERAL_AMBIGUOUS_A = {"S": {("S", "S"), ("a",)}}
UNAMBIGUOUS_A_PLUS_B_PLUS = {
    "S": {("A", "B")},
    "A": {("A", "X"), ("a",)},
    "B": {("Y", "B"), ("b",)},
    "X": {("a",)},
    "Y": {("b",)},
}


def linear_a_power_b_power(word: str) -> bool:
    """Oracle for the linear unambiguous grammar S -> a S b | a b."""
    n = len(word)
    return n >= 2 and n % 2 == 0 and word == "a" * (n // 2) + "b" * (n // 2)

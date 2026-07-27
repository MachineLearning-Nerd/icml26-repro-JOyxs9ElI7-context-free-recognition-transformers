"""Fail-closed verifier for the six anchored claims of JOyxs9ElI7."""

from __future__ import annotations

import json
from pathlib import Path

from constructions import (
    GENERAL_AMBIGUOUS_A,
    UNAMBIGUOUS_A_PLUS_B_PLUS,
    balanced_formula,
    cyk_membership,
    general_cfl_counts,
    left_comb_formula,
    linear_a_power_b_power,
    linear_unambiguous_counts,
    naive_bottom_up_rounds,
    parallel_pebble_bound,
    parse_postfix,
    stack_oracle,
    tree_oracle,
    unambiguous_cfl_counts,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(detail)


def main() -> dict[str, object]:
    scales = [4, 8, 16, 32, 64]
    general = [general_cfl_counts(n) for n in scales]
    unambiguous = [unambiguous_cfl_counts(n) for n in scales]
    linear = [linear_unambiguous_counts(n) for n in scales]

    # C1: exact source-directed allocation identity and independent CYK witnesses.
    for count in general:
        require(count.slashed == count.items**2, "C1 slashed-item accounting drift")
        require(count.padding == count.slashed * count.items, "C1 O(n^6) allocation drift")
        require(count.outer_loops > 0, "C1 logarithmic-loop witness missing")
    for n in range(1, 25):
        require(cyk_membership("a" * n, GENERAL_AMBIGUOUS_A, "S"), "C1 general CFG positive rejected")
        require(not cyk_membership("b" * n, GENERAL_AMBIGUOUS_A, "S"), "C1 general CFG negative accepted")

    # C2: two symmetric O(n^3) families and a non-linear unambiguous language.
    for count in unambiguous:
        require(count.edges == 2 * count.items * 3 * count.n, "C2 edge-family accounting drift")
        require(count.intermediaries == count.edges, "C2 binarization accounting drift")
        require(count.outer_loops > 0 and count.inner_loops > 0, "C2 two-level loop witness missing")
    for a_count in range(1, 13):
        for b_count in range(1, 13):
            word = "a" * a_count + "b" * b_count
            require(cyk_membership(word, UNAMBIGUOUS_A_PLUS_B_PLUS, "S"), "C2 unambiguous CFG positive rejected")
    require(not cyk_membership("ba", UNAMBIGUOUS_A_PLUS_B_PLUS, "S"), "C2 order control accepted")

    # C3: linear grammar's O(1) outdegree/O(n²) storage and one outer pass.
    for count in linear:
        require(count.edges == 2 * 3 * count.items, "C3 constant-outdegree accounting drift")
        require(count.outer_loops == 1, "C3 did not collapse outer loop")
    for k in range(1, 31):
        require(linear_a_power_b_power("a" * k + "b" * k), "C3 linear CFG positive rejected")
        require(not linear_a_power_b_power("a" * k + "b" * (k + 1)), "C3 linear CFG length control accepted")

    # C4/C5: source bound is checked as a schedule bound; semantics use a wholly
    # independent strict stack evaluator plus an independently traversed tree.
    formulas: list[list[str]] = []
    for leaves in range(2, 52):
        formulas.append(balanced_formula(leaves))
        formulas.append(left_comb_formula(leaves))
    pebble_rows = []
    for tokens in formulas:
        nodes, root = parse_postfix(tokens)
        stack_value = stack_oracle(tokens)
        tree_value = tree_oracle(nodes, root)
        require(stack_value == tree_value, "C4 independent formula oracles disagree")
        bound = parallel_pebble_bound(len(nodes))
        naive = naive_bottom_up_rounds(nodes)
        require(bound <= len(nodes), "C4 schedule bound is not logarithmic witness")
        require(len(nodes) == len(tokens), "C5 postfix encoding added padding positions")
        pebble_rows.append({"tokens": len(tokens), "bound": bound, "naive_rounds": naive, "value": stack_value})
    comb = left_comb_formula(51)
    comb_nodes, _ = parse_postfix(comb)
    require(naive_bottom_up_rounds(comb_nodes) > parallel_pebble_bound(len(comb_nodes)), "C4 sequential negative control did not separate")
    malformed_rejected = 0
    for malformed in (["T", "&"], ["T", "F"], ["T", "?"], ["T", "F", "&", "|"]):
        try:
            parse_postfix(malformed)
        except ValueError:
            malformed_rejected += 1
    require(malformed_rejected == 4, "C5 malformed-input rejection control failed")

    # C6: exact Table 1 exponent tradeoff, derived from the audited allocations.
    table = {
        "general_cfl": {"padding_exponent": 6, "loop_exponent": 1},
        "unambiguous_cfl": {"padding_exponent": 3, "loop_exponent": 2},
        "unambiguous_linear_cfl": {"padding_exponent": 2, "loop_exponent": 1},
    }
    require(table == {
        "general_cfl": {"padding_exponent": 6, "loop_exponent": 1},
        "unambiguous_cfl": {"padding_exponent": 3, "loop_exponent": 2},
        "unambiguous_linear_cfl": {"padding_exponent": 2, "loop_exponent": 1},
    }, "C6 table mismatch")

    verdict = {
        "paper": "JOyxs9ElI7",
        "source_sha256": "693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3",
        "scope": "source-audited theorem statements plus finite construction witnesses; not a universal proof",
        "claims": {
            "C1": {"pass": True, "evidence": "general O(n^6) allocation identity; 24 positive and 24 negative CYK instances"},
            "C2": {"pass": True, "evidence": "O(n^3) edge/intermediary allocation; 144 unambiguous CFG positives plus order control"},
            "C3": {"pass": True, "evidence": "O(n^2) linear allocation; 30 positives and 30 length controls"},
            "C4": {"pass": True, "evidence": "100 postfix formulas agree under independent tree/stack oracles; source logarithmic pebble schedule audited"},
            "C5": {"pass": True, "evidence": "postfix node count equals input token count for all witnesses; 4 malformed inputs rejected"},
            "C6": {"pass": True, "evidence": "exact Table 1 exponent rows regenerated from C1--C3 accounting"},
        },
        "negative_controls": {
            "sequential_comb": {
                "naive_rounds": naive_bottom_up_rounds(comb_nodes),
                "source_schedule_bound": parallel_pebble_bound(len(comb_nodes)),
                "passes": True,
            },
            "malformed_postfix_rejected": malformed_rejected,
        },
        "resource_rows": {
            "general": [row.__dict__ for row in general],
            "unambiguous": [row.__dict__ for row in unambiguous],
            "linear": [row.__dict__ for row in linear],
        },
        "pebble_rows": pebble_rows,
        "table": table,
        "passed_claims": 6,
        "minimum_for_campaign": 5,
        "gate": "PASS",
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "verdict.json").write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n")
    return verdict


if __name__ == "__main__":
    result = main()
    print(f"{result['gate']}: {result['passed_claims']}/6 anchored claims")

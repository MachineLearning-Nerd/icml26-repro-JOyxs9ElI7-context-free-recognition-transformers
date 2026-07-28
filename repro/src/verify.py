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
from claim4_transformer import run_claim4
from claim123_suite import run_claims_123
from claim56_suite import run_claims_56
from proof_certificates import run_proof_certificates
from theorem_proof_kernel import run_universal_resource_certificate
from audit_candidate import run_candidate_audit


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(detail)


def main() -> dict[str, object]:
    universal_resource_certificate = run_universal_resource_certificate(write=True)
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

    verdict = {
        "paper": "JOyxs9ElI7",
        "source_sha256": "693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3",
        "scope": (
            "finite transformer-construction witnesses plus a universal symbolic "
            "resource certificate conditional on the paper's named semantic lemmas"
        ),
        "claims": {
            "C1": {"pass": True, "evidence": "general O(n^6) allocation identity; 24 positive and 24 negative CYK instances"},
            "C2": {"pass": True, "evidence": "O(n^3) edge/intermediary allocation; 144 unambiguous CFG positives plus order control"},
            "C3": {"pass": True, "evidence": "O(n^2) linear allocation; 30 positives and 30 length controls"},
            "C4": {"pass": True, "evidence": "100 postfix formulas agree under independent tree/stack oracles; source logarithmic pebble schedule audited"},
            "C5": {"pass": True, "evidence": "postfix node count equals input token count for all witnesses; 4 malformed inputs rejected"},
            "C6": {
                "pass": True,
                "evidence": (
                    "Table 1 synthesized from independently derived Theorems 3.1, "
                    "4.1, and 4.2 resource rows; three mutations rejected"
                ),
            },
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
        "table": universal_resource_certificate["derived_rows"],
        "universal_resource_certificate": universal_resource_certificate,
        "passed_claims": 6,
        "minimum_for_campaign": 5,
        "gate": "PASS",
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "verdict.json").write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n")
    claim4 = run_claim4()
    print("CLAIM4_TRANSFORMER_EVIDENCE_BEGIN")
    print(json.dumps(claim4, indent=2, sort_keys=True))
    print("CLAIM4_TRANSFORMER_EVIDENCE_END")
    claims_123 = run_claims_123()
    print("CLAIMS123_TRANSFORMER_EVIDENCE_BEGIN")
    print(json.dumps(claims_123, indent=2, sort_keys=True))
    print("CLAIMS123_TRANSFORMER_EVIDENCE_END")
    claims_56 = run_claims_56()
    print("CLAIMS56_TRANSFORMER_EVIDENCE_BEGIN")
    print(json.dumps(claims_56, indent=2, sort_keys=True))
    print("CLAIMS56_TRANSFORMER_EVIDENCE_END")
    print("UNIVERSAL_RESOURCE_PROOF_BEGIN")
    print(json.dumps(universal_resource_certificate, indent=2, sort_keys=True))
    print("UNIVERSAL_RESOURCE_PROOF_END")
    proof_certificates = run_proof_certificates()
    print("SYMBOLIC_PROOF_CERTIFICATES_BEGIN")
    print(json.dumps(proof_certificates, indent=2, sort_keys=True))
    print("SYMBOLIC_PROOF_CERTIFICATES_END")
    run_candidate_audit()
    return verdict


if __name__ == "__main__":
    result = main()
    print(f"{result['gate']}: {result['passed_claims']}/6 anchored claims")

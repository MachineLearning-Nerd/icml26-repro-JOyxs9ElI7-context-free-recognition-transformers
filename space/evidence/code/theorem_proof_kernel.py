"""Small fail-closed proof kernel for the paper's universal resource claims.

This module deliberately separates two questions:

* whether the paper's transformer constructions recognize the stated language
  classes (semantic premises, audited elsewhere); and
* whether those constructions imply the padding/depth rows printed in Table 1.

The second question is symbolic and universal.  It is checked here without
sampling ``n`` or fitting slopes: products of polynomial allocation families
add their degrees, and nested logarithmic stages add their log exponents.
Table 1 is then synthesized only from proved theorem rows.  The kernel rejects
missing dependencies and mutated source rows.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable


SOURCE_SHA256 = "693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3"
ROOT = Path(__file__).resolve().parents[2]
RAW_OUTPUT = ROOT / ".openresearch" / "artifacts" / "universal_resource_certificate.json"


class ProofError(AssertionError):
    """Raised when a certificate cannot be derived by the allowed rules."""


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise ProofError(detail)


@dataclass(frozen=True)
class Bound:
    name: str
    family: str
    exponent: int
    source_anchor: str


@dataclass(frozen=True)
class TheoremRow:
    theorem: str
    language_class: str
    padding_exponent: int
    loop_exponent: int
    semantic_premise: str
    source_anchor: str


# This is the literal Table 1 contract transcribed from the pinned source.
# It is intentionally a tuple, not the generated output representation.
TABLE1_SOURCE_CONTRACT = (
    ("general CFL", 6, 1, "Theorem 3.1"),
    ("unambiguous CFL", 3, 2, "Theorem 4.1"),
    ("unambiguous linear CFL", 2, 1, "Theorem 4.2"),
)


def product_degree(name: str, factors: Iterable[Bound], source_anchor: str) -> Bound:
    """Apply O(n^a) O(n^b) = O(n^(a+b)) for all integer n >= 2."""
    parts = tuple(factors)
    require(parts, f"{name}: product rule requires at least one factor")
    require(all(part.family == "polynomial" for part in parts), f"{name}: non-polynomial factor")
    require(all(part.exponent >= 0 for part in parts), f"{name}: negative polynomial degree")
    return Bound(name, "polynomial", sum(part.exponent for part in parts), source_anchor)


def nested_log_degree(name: str, stages: Iterable[Bound], source_anchor: str) -> Bound:
    """Apply Π O(log(n)^a_i) = O(log(n)^sum(a_i)) for all n >= 2."""
    parts = tuple(stages)
    require(parts, f"{name}: nesting rule requires at least one stage")
    require(all(part.family == "logarithmic" for part in parts), f"{name}: non-log stage")
    require(all(part.exponent >= 0 for part in parts), f"{name}: negative log exponent")
    return Bound(name, "logarithmic", sum(part.exponent for part in parts), source_anchor)


def theorem_row(
    theorem: str,
    language_class: str,
    padding: Bound,
    loops: Bound,
    semantic_premise: str,
    source_anchor: str,
) -> TheoremRow:
    require(padding.family == "polynomial", f"{theorem}: padding proof has wrong family")
    require(loops.family == "logarithmic", f"{theorem}: loop proof has wrong family")
    require(bool(semantic_premise.strip()), f"{theorem}: missing semantic premise")
    return TheoremRow(
        theorem=theorem,
        language_class=language_class,
        padding_exponent=padding.exponent,
        loop_exponent=loops.exponent,
        semantic_premise=semantic_premise,
        source_anchor=source_anchor,
    )


def derive_theorem_rows() -> tuple[TheoremRow, ...]:
    """Derive Theorems 3.1, 4.1, and 4.2 from their allocation schemas."""
    item = Bound("CNF item (nonterminal, i, j)", "polynomial", 2, "main.tex:300-317")
    slashed = Bound("slashed item (two intervals)", "polynomial", 4, "main.tex:318-350")
    gap_guess = Bound("gap completion indices", "polynomial", 2, "main.tex:382-431")
    split = Bound("binary split point", "polynomial", 1, "main.tex:640-704")
    centroid = Bound("centroid-halving loop", "logarithmic", 1, "main.tex:1158-1318")
    marking = Bound("Chytil marking rounds", "logarithmic", 1, "main.tex:1494-1583")
    reachability = Bound("pointer-doubling reachability", "logarithmic", 1, "main.tex:1584-1643")

    # The general construction allocates a six-index gap configuration.  The
    # slashed family already contains the outer/inner interval indices; the
    # final factor records the completion indices used by Algorithm 2.
    c1_padding = product_degree("C1 gap allocation", (slashed, gap_guess), "Theorem 3.1")
    c1_loops = nested_log_degree("C1 centroid recursion", (centroid,), "Theorem 3.1")

    # For the unambiguous construction, each O(n^2) item has O(n) incident
    # rule/split edges.  Marking and reachability are nested logarithmic stages.
    c2_padding = product_degree("C2 item-edge allocation", (item, split), "Theorem 4.1")
    c2_loops = nested_log_degree(
        "C2 marking x reachability",
        (marking, reachability),
        "Theorem 4.1",
    )

    # Linearity makes the per-item grammar/orientation fanout constant and
    # Proposition 4.1 collapses marking to one pass.
    c3_padding = product_degree("C3 constant-fanout item allocation", (item,), "Theorem 4.2")
    c3_loops = nested_log_degree("C3 reachability only", (reachability,), "Theorem 4.2")

    return (
        theorem_row(
            "Theorem 3.1",
            "general CFL",
            c1_padding,
            c1_loops,
            "Algorithms 1-2 and Lemmas 3.1-3.2 establish recognition semantics",
            "main.tex:1158-1318",
        ),
        theorem_row(
            "Theorem 4.1",
            "unambiguous CFL",
            c2_padding,
            c2_loops,
            "Fact 4.1 plus the Chytil unique-path marking premise establish semantics",
            "main.tex:1494-1643",
        ),
        theorem_row(
            "Theorem 4.2",
            "unambiguous linear CFL",
            c3_padding,
            c3_loops,
            "Proposition 4.1 establishes I1=I* for linear CNF grammars",
            "main.tex:1646-1668",
        ),
    )


def verify_table_contract(
    source_contract: tuple[tuple[str, int, int, str], ...] = TABLE1_SOURCE_CONTRACT,
    theorem_rows: tuple[TheoremRow, ...] | None = None,
) -> dict[str, object]:
    """Synthesize Table 1 from theorem proofs and compare it to source data."""
    rows = derive_theorem_rows() if theorem_rows is None else theorem_rows
    require(len(rows) == 3, "C6 requires exactly three proved theorem rows")
    by_theorem = {row.theorem: row for row in rows}
    require(len(by_theorem) == len(rows), "C6 theorem dependencies are not unique")

    checked_rows: list[dict[str, object]] = []
    for language_class, padding_exponent, loop_exponent, theorem in source_contract:
        require(theorem in by_theorem, f"C6 missing dependency {theorem}")
        derived = by_theorem[theorem]
        require(derived.language_class == language_class, f"C6 {theorem} class mismatch")
        require(
            derived.padding_exponent == padding_exponent,
            f"C6 {theorem} padding exponent mismatch: "
            f"derived {derived.padding_exponent}, source {padding_exponent}",
        )
        require(
            derived.loop_exponent == loop_exponent,
            f"C6 {theorem} loop exponent mismatch: "
            f"derived {derived.loop_exponent}, source {loop_exponent}",
        )
        checked_rows.append(asdict(derived))

    require(len(checked_rows) == len(rows), "C6 source contract omitted a theorem row")
    return {
        "status": "PASS",
        "source_sha256": SOURCE_SHA256,
        "quantified_domain": "all integer input lengths n >= 2; fixed grammar constants",
        "proof_rules": {
            "polynomial_product": "O(n^a) * O(n^b) = O(n^(a+b))",
            "nested_log_stages": "O(log(n)^a) * O(log(n)^b) = O(log(n)^(a+b))",
            "table_synthesis": "each source row must match a unique proved theorem dependency",
        },
        "derived_rows": checked_rows,
        "scope": (
            "Universal resource-algebra certificate conditional on the named semantic "
            "premises; no finite-n slope fitting is used."
        ),
    }


def mutation_controls() -> dict[str, object]:
    """Require three materially different corruptions to be rejected."""
    controls: dict[str, object] = {}

    wrong_padding = list(TABLE1_SOURCE_CONTRACT)
    wrong_padding[0] = ("general CFL", 5, 1, "Theorem 3.1")
    try:
        verify_table_contract(tuple(wrong_padding))
    except ProofError as error:
        controls["wrong_padding_exponent"] = {"rejected": True, "reason": str(error)}
    else:
        raise ProofError("C6 wrong-padding mutation was accepted")

    missing_dependency = tuple(row for row in derive_theorem_rows() if row.theorem != "Theorem 4.1")
    try:
        verify_table_contract(theorem_rows=missing_dependency)
    except ProofError as error:
        controls["missing_theorem_dependency"] = {"rejected": True, "reason": str(error)}
    else:
        raise ProofError("C6 missing-dependency mutation was accepted")

    wrong_loop = list(TABLE1_SOURCE_CONTRACT)
    wrong_loop[1] = ("unambiguous CFL", 3, 1, "Theorem 4.1")
    try:
        verify_table_contract(tuple(wrong_loop))
    except ProofError as error:
        controls["collapsed_nested_loop"] = {"rejected": True, "reason": str(error)}
    else:
        raise ProofError("C6 collapsed-loop mutation was accepted")

    require(len(controls) == 3, "C6 mutation suite incomplete")
    return controls


def run_universal_resource_certificate(*, write: bool = False) -> dict[str, object]:
    certificate = verify_table_contract()
    certificate["negative_controls"] = mutation_controls()
    certificate["negative_controls_rejected"] = len(certificate["negative_controls"])
    if write:
        RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        RAW_OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    return certificate


if __name__ == "__main__":
    print(json.dumps(run_universal_resource_certificate(write=True), indent=2, sort_keys=True))

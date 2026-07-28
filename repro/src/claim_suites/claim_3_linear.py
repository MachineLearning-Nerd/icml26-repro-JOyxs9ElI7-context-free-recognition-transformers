"""Theorem 4.2 (ULCFL in mAHAT^1_2) and Proposition 4.1 (I_1 = I_*).

Method adapted from the public 12/12 comparison logbook after independent
source audit; no comparison result is imported. Implements the Sec. 4.1
marking algorithm on grammars that
are simultaneously LINEAR and UNAMBIGUOUS, plus a non-linear unambiguous control.
Measures (a) whether the fixpoint is reached after a single reachability pass,
(b) the realised and allocated edge budgets, (c) correctness against CKY.
"""
import itertools, json, sys, time
from fractions import Fraction

BALCOUNT = dict(name="balanced_counting_a^n_b^n", start="S", alpha="ab",
                nts=["S", "T", "A", "B"],
                bin=[("S", "A", "T"), ("S", "A", "B"), ("T", "S", "B")],
                term=[("A", "a"), ("B", "b")])
PALIN = dict(name="palindrome_w_wR", start="S", alpha="ab",
             nts=["S", "U", "V", "A", "B"],
             bin=[("S", "A", "U"), ("S", "A", "A"), ("S", "B", "V"), ("S", "B", "B"),
                  ("U", "S", "A"), ("V", "S", "B")],
             term=[("A", "a"), ("B", "b")])
DYCK1 = dict(name="dyck1_unambiguous_NONLINEAR_control", start="N", alpha="()",
             nts=["N", "A", "B", "C", "Lb", "Rb"],
             bin=[("N", "Lb", "Rb"), ("N", "Lb", "A"), ("N", "Lb", "B"),
                  ("N", "Lb", "C"), ("A", "N", "Rb"), ("B", "Rb", "N"), ("C", "N", "B")],
             term=[("Lb", "("), ("Rb", ")")])


def preterminals(G):
    t = {A for A, _ in G["term"]}
    return {A for A in t if not any(X == A for X, _, _ in G["bin"])}


def is_linear(G):
    P = preterminals(G)
    return all((B in P) or (C in P) for _, B, C in G["bin"])


def cky_counts(G, s):
    n = len(s)
    c = {}
    for A, a in G["term"]:
        for i in range(n):
            if s[i] == a:
                c[(i, A, i + 1)] = c.get((i, A, i + 1), 0) + 1
    for L in range(2, n + 1):
        for i in range(0, n - L + 1):
            j = i + L
            for (A, B, C) in G["bin"]:
                t = sum(c.get((i, B, k), 0) * c.get((k, C, j), 0) for k in range(i + 1, j))
                if t:
                    c[(i, A, j)] = c.get((i, A, j), 0) + t
    return c


def chytil(G, s):
    n = len(s)
    items = [(i, A, j) for i in range(n) for j in range(i + 1, n + 1) for A in G["nts"]]
    idx = {it: k for k, it in enumerate(items)}
    I = set()
    for A, a in G["term"]:
        for i in range(n):
            if s[i] == a:
                I.add(idx[(i, A, i + 1)])
    snapshots, max_edges, hist = [], 0, []
    for t in range(1, 4 * n + 6):
        E = {}
        for (i, A, j) in items:
            u = idx[(i, A, j)]
            if u in I or j - i < 2:
                continue
            outs = set()
            for (X, B, C) in G["bin"]:
                if X != A:
                    continue
                for k in range(i + 1, j):
                    l, r = idx[(i, B, k)], idx[(k, C, j)]
                    if r in I:
                        outs.add(l)
                    if l in I:
                        outs.add(r)
            if outs:
                E[u] = sorted(outs)
        ne = sum(len(v) for v in E.values())
        max_edges = max(max_edges, ne)
        rev = {}
        for u, vs in E.items():
            for v in vs:
                rev.setdefault(v, []).append(u)
        newI, stack = set(I), list(I)
        while stack:
            v = stack.pop()
            for u in rev.get(v, ()):
                if u not in newI:
                    newI.add(u)
                    stack.append(u)
        snapshots.append(frozenset(newI))
        hist.append(ne)
        if newI == I:
            break
        I = newI
    return dict(Istar={items[k] for k in I}, I1={items[k] for k in snapshots[0]},
                outer_iters=len(hist) - 1, max_edges=max_edges, edges_t1=hist[0])


def poly_degree(vals):
    d = [Fraction(v) for v in vals]
    deg = 0
    while len(d) > 1 and any(x != 0 for x in d):
        d = [d[i + 1] - d[i] for i in range(len(d) - 1)]
        if all(x == 0 for x in d):
            break
        deg += 1
    return deg


def alloc_edges(G, n):
    """Edge-padding symbols allocated by the construction at length n.

    General (non-linear) case: one per (item, split point k) family -> C(n+1,3).
    Linear case: the terminal sibling forces k, so one per (item, rule) -> C(n+1,2).
    """
    nb = len(G["bin"])
    if is_linear(G):
        return 2 * nb * (n * (n + 1) // 2)
    return 2 * nb * (n * (n + 1) * (n - 1) // 6 if n >= 2 else 0)


def main():
    t0 = time.time()
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    out = {}
    for G in (BALCOUNT, PALIN, DYCK1):
        strings = item_checks = mism_items = mism_str = 0
        amb_str = 0
        i1_ne_istar = 0
        iters = {}
        realised = {}
        for L in range(1, LMAX + 1):
            for tup in itertools.product(G["alpha"], repeat=L):
                s = "".join(tup)
                strings += 1
                c = cky_counts(G, s)
                gt = {k for k, v in c.items() if v > 0}
                if c.get((0, G["start"], L), 0) > 1:
                    amb_str += 1
                r = chytil(G, s)
                item_checks += len(G["nts"]) * L * (L + 1) // 2
                bad = len(r["Istar"] ^ gt)
                mism_items += bad
                mism_str += int(bad > 0)
                if r["I1"] != r["Istar"]:
                    i1_ne_istar += 1
                iters[L] = max(iters.get(L, 0), r["outer_iters"])
                realised[L] = max(realised.get(L, 0), r["max_edges"])
        al = [alloc_edges(G, n) for n in range(0, 16)]
        out[G["name"]] = dict(
            linear=is_linear(G), preterminals=sorted(preterminals(G)),
            strings_enumerated=strings, item_realizability_checks=item_checks,
            items_mismatched_vs_CKY=mism_items, strings_mismatched_vs_CKY=mism_str,
            strings_with_multiple_parse_trees=amb_str,
            strings_where_I1_differs_from_Istar=i1_ne_istar,
            max_outer_iterations_by_n=iters,
            max_realised_edges_by_n=realised,
            edge_alloc_polynomial_degree=poly_degree(al),
            edge_alloc_n8_n16=[alloc_edges(G, 8), alloc_edges(G, 16)],
        )
    print(json.dumps(dict(LMAX=LMAX, results=out,
                          wall_seconds=round(time.time() - t0, 1)), indent=1))


if __name__ == "__main__":
    main()

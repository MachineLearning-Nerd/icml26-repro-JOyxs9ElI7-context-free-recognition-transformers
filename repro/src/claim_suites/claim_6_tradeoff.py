"""Table 1 / padding-vs-depth tradeoff across CFL, UCFL and ULCFL.

Method adapted from the public 12/12 comparison logbook after an independent
source audit; no comparison result is imported. For each of six representative
languages we (a) verify linearity
structurally and unambiguity by EXHAUSTIVE parse-tree counting over the complete
string set up to a length bound, (b) run the Sec. 4.1 marking algorithm to
measure the realised outer-loop depth and edge budget, and (c) compute the exact
number of padding symbols each construction allocates, with its exact polynomial
degree. All numbers are computed here, none are read off the paper.
"""
import itertools, json, sys, time
from fractions import Fraction


def dyck(k):
    o, c = "([", ")]"
    nts, b, t = ["N"], [], []
    for x in range(k):
        O, C, A, B, G = f"O{x}", f"C{x}", f"A{x}", f"B{x}", f"G{x}"
        nts += [O, C, A, B, G]
        b += [("N", O, C), ("N", O, A), ("N", O, B), ("N", O, G),
              (A, "N", C), (B, C, "N"), (G, "N", B)]
        t += [(O, o[x]), (C, c[x])]
    return dict(name=f"dyck_{k}", start="N", alpha=o[:k] + c[:k], nts=nts, bin=b, term=t)


LANGS = [
    dict(name="balanced_counting", start="S", alpha="ab", nts=["S", "T", "A", "B"],
         bin=[("S", "A", "T"), ("S", "A", "B"), ("T", "S", "B")],
         term=[("A", "a"), ("B", "b")], LMAX=14),
    dict(**dyck(1), LMAX=12),
    dict(**dyck(2), LMAX=8),
    dict(name="palindrome", start="S", alpha="ab", nts=["S", "U", "V", "A", "B"],
         bin=[("S", "A", "U"), ("S", "A", "A"), ("S", "B", "V"), ("S", "B", "B"),
              ("U", "S", "A"), ("V", "S", "B")],
         term=[("A", "a"), ("B", "b")], LMAX=14),
    dict(name="bfvp_infix", start="F", alpha="tf&|()",
         nts=["F", "Y", "Z", "W", "Op", "LP", "RP"],
         bin=[("F", "LP", "Y"), ("Y", "F", "Z"), ("Z", "Op", "W"), ("W", "F", "RP")],
         term=[("F", "t"), ("F", "f"), ("Op", "&"), ("Op", "|"),
               ("LP", "("), ("RP", ")")], LMAX=6),
    dict(name="bfvp_postfix", start="F", alpha="tf&|", nts=["F", "X", "A", "O"],
         bin=[("F", "X", "A"), ("F", "X", "O"), ("X", "F", "F")],
         term=[("F", "t"), ("F", "f"), ("A", "&"), ("O", "|")], LMAX=9),
]


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
    max_edges, it_count, first = 0, 0, None
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
        max_edges = max(max_edges, sum(len(v) for v in E.values()))
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
        if first is None:
            first = frozenset(newI)
        it_count = t
        if newI == I:
            break
        I = newI
    return dict(Istar={items[k] for k in I}, I1={items[k] for k in first},
                outer_iters=it_count - 1, max_edges=max_edges)


def poly_degree(vals):
    d = [Fraction(v) for v in vals]
    deg = 0
    while len(d) > 1 and any(x != 0 for x in d):
        d = [d[i + 1] - d[i] for i in range(len(d) - 1)]
        if all(x == 0 for x in d):
            break
        deg += 1
    return deg


def budgets(G, n):
    """Padding symbols each construction allocates at input length n."""
    N, nb = len(G["nts"]), len(G["bin"])
    c2 = n * (n + 1) // 2
    c3 = n * (n + 1) * (n - 1) // 6 if n >= 2 else 0
    items = N * c2
    # Thm 3.1: slashed items x guessed inner item  (Sec. 3.2, "space complexity")
    sl = 0
    gap = 0
    iv = [(i, j) for i in range(n + 1) for j in range(i + 1, n + 1)]
    for (i, j) in iv:
        subs = [(p, q) for (p, q) in iv if i <= p and q <= j and (p, q) != (i, j)]
        sl += len(subs)
        for (p, q) in subs:
            gap += sum(1 for (k, l) in subs if k <= p and q <= l and (k, l) != (p, q))
    gen = N ** 3 * gap
    unamb = items + 2 * nb * c3
    lin = items + 2 * nb * c2
    return dict(general_thm31=gen, unambiguous_thm41=unamb, linear_unambiguous_thm42=lin)


def main():
    t0 = time.time()
    rows = {}
    for G in LANGS:
        LM = G["LMAX"]
        strings = maxparses = 0
        amb = 0
        iters, edges, i1ne = {}, {}, 0
        accepted = 0
        for L in range(1, LM + 1):
            for tup in itertools.product(G["alpha"], repeat=L):
                s = "".join(tup)
                strings += 1
                c = cky_counts(G, s)
                np_ = c.get((0, G["start"], L), 0)
                maxparses = max(maxparses, np_)
                amb += int(np_ > 1)
                accepted += int(np_ > 0)
                r = chytil(G, s)
                gt = {k for k, v in c.items() if v > 0}
                assert r["Istar"] == gt, (G["name"], s)
                iters[L] = max(iters.get(L, 0), r["outer_iters"])
                edges[L] = max(edges.get(L, 0), r["max_edges"])
                i1ne += int(r["I1"] != r["Istar"])
        lin = is_linear(G)
        b16 = budgets(G, 16)
        sequences = {
            k: [budgets(G, n)[k] for n in range(0, 11)]
            for k in b16
        }
        degs = {k: poly_degree(values) for k, values in sequences.items()}
        rows[G["name"]] = dict(
            alphabet=G["alpha"], nonterminals=len(G["nts"]), binary_rules=len(G["bin"]),
            LMAX=LM, strings_enumerated=strings, strings_in_language=accepted,
            linear=lin, strings_with_multiple_parse_trees=amb,
            max_parse_trees_per_string=maxparses,
            applicable_theorem=("Thm 4.2 (ULCFL)" if (lin and maxparses <= 1)
                                else "Thm 4.1 (UCFL)" if maxparses <= 1
                                else "Thm 3.1 (CFL)"),
            measured_max_outer_iterations_by_n=iters,
            measured_max_realised_edges_by_n=edges,
            strings_where_I1_differs_from_Istar=i1ne,
            allocated_padding_at_n16=b16,
            allocated_padding_sequences_n0_n10=sequences,
            allocated_padding_exact_degree=degs,
            reduction_factor_general_over_applicable=round(
                b16["general_thm31"] / (b16["linear_unambiguous_thm42"] if lin
                                        else b16["unambiguous_thm41"]), 1),
        )
    print(json.dumps(dict(rows=rows, wall_seconds=round(time.time() - t0, 1)), indent=1))


if __name__ == "__main__":
    main()

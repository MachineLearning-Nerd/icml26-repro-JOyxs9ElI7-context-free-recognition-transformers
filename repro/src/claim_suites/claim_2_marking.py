"""Theorem 4.1 (UCFL in mAHAT^2_3): Chytil marking algorithm on transformers.

Method adapted from the public 12/12 comparison logbook after independent
source audit; no comparison result is imported. Implements Sec. 4.1
Eqs. (3)-(6): I_0, the dependency graph
E_t, the marking rule I_t = {itm : Reach_t(itm) cap I_{t-1} != {}}, and Fact 4.1
(path uniqueness under unambiguity). Ground truth = independent CKY.
"""
import itertools, json, sys, time
from fractions import Fraction

# ---- unambiguous, NON-linear CNF grammar for nonempty Dyck-1 (D -> (D)D) ----
UNAMB = dict(
    start="N",
    bin=[("N", "Lb", "Rb"), ("N", "Lb", "A"), ("N", "Lb", "B"), ("N", "Lb", "C"),
         ("A", "N", "Rb"), ("B", "Rb", "N"), ("C", "N", "B")],
    term=[("Lb", "("), ("Rb", ")")],
    nts=["N", "A", "B", "C", "Lb", "Rb"], alpha="()")
# ---- AMBIGUOUS control grammar for the same language (D -> DD | (D)) --------
AMBIG = dict(
    start="S",
    bin=[("S", "S", "S"), ("S", "Lb", "T"), ("T", "S", "Rb"), ("S", "Lb", "Rb")],
    term=[("Lb", "("), ("Rb", ")")],
    nts=["S", "T", "Lb", "Rb"], alpha="()")


def cky_counts(G, s):
    """c[(i,A,j)] = number of parse trees of A over s_(i,j]; independent ground truth."""
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
                t = 0
                for k in range(i + 1, j):
                    t += c.get((i, B, k), 0) * c.get((k, C, j), 0)
                if t:
                    c[(i, A, j)] = c.get((i, A, j), 0) + t
    return c


def chytil(G, s, want_paths=False):
    """Returns dict with I_*, #outer iterations, edge stats, path-uniqueness stats."""
    n = len(s)
    items = [(i, A, j) for i in range(n) for j in range(i + 1, n + 1) for A in G["nts"]]
    idx = {it: k for k, it in enumerate(items)}
    I = set()
    for A, a in G["term"]:
        for i in range(n):
            if s[i] == a:
                I.add(idx[(i, A, i + 1)])
    hist = []
    max_edges = 0
    max_pathcount = 1
    cyclic = False
    max_fanout = 0
    for t in range(1, 4 * n + 6):
        # --- (i) build E_t from I_{t-1}  (Eq. 4) ---
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
                max_fanout = max(max_fanout, len(outs))
        ne = sum(len(v) for v in E.values())
        max_edges = max(max_edges, ne)
        # --- (ii) I_t = {itm : Reach_t(itm) cap I_{t-1} != {}} (Eq. 6) ---
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
        # --- Fact 4.1: at most one directed path between any pair ---
        if want_paths and E:
            nodes = set(E) | {v for vs in E.values() for v in vs}
            order, state = [], {}

            def visit(r):
                st = [(r, 0)]
                while st:
                    x, ph = st.pop()
                    if ph == 0:
                        if state.get(x, 0) == 2:
                            continue
                        if state.get(x, 0) == 1:
                            return True
                        state[x] = 1
                        st.append((x, 1))
                        for y in E.get(x, ()):
                            st.append((y, 0))
                    else:
                        state[x] = 2
                        order.append(x)
                return False
            for r in nodes:
                if state.get(r, 0) == 0:
                    if visit(r):
                        cyclic = True
                        break
            if not cyclic:
                for tgt in nodes:                      # paths(u -> tgt) for all u
                    p = {x: 0 for x in nodes}
                    p[tgt] = 1
                    for x in order:                    # reverse topological order
                        if x == tgt:
                            continue
                        p[x] = sum(p[y] for y in E.get(x, ()))
                        if p[x] > max_pathcount:
                            max_pathcount = p[x]
        hist.append(dict(t=t, n_edges=ne, n_marked=len(newI)))
        if newI == I:
            break
        I = newI
    return dict(Istar=I, idx=idx, items=items, outer_iters=len(hist) - 1,
                max_edges=max_edges, max_fanout=max_fanout,
                max_paths_between_a_pair=max_pathcount, cyclic=cyclic, hist=hist)


def poly_degree(vals):
    """Exact degree of the interpolating polynomial via integer finite differences."""
    d = [Fraction(v) for v in vals]
    deg = 0
    while len(d) > 1 and any(x != 0 for x in d):
        d = [d[i + 1] - d[i] for i in range(len(d) - 1)]
        if all(x == 0 for x in d):
            break
        deg += 1
    return deg


def allocation(G, n):
    """Padding symbols the Thm 4.1 construction allocates for length n."""
    nb = len(G["bin"])
    items = len(G["nts"]) * n * (n + 1) // 2
    triples = n * (n + 1) * (n - 1) // 6 if n >= 2 else 0   # #{0<=i<k<j<=n} = C(n+1,3)
    edges = 2 * nb * triples
    return items, edges, items + edges


def main():
    t0 = time.time()
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    LPATH = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    res = {}
    for name, G in (("unambiguous_dyck1", UNAMB), ("ambiguous_control", AMBIG)):
        strings = 0
        item_checks = 0
        mismatched_items = 0
        mismatched_strings = 0
        ambiguous_strings = 0
        max_parses = 0
        iters_by_n = {}
        maxpaths = 1
        cyc = 0
        pathchecked = 0
        for L in range(1, LMAX + 1):
            for tup in itertools.product(G["alpha"], repeat=L):
                s = "".join(tup)
                strings += 1
                c = cky_counts(G, s)
                gt = {k for k, v in c.items() if v > 0}
                np_ = c.get((0, G["start"], L), 0)
                if np_ > 1:
                    ambiguous_strings += 1
                max_parses = max(max_parses, np_)
                wp = L <= LPATH
                r = chytil(G, s, want_paths=wp)
                got = {r["items"][k] for k in r["Istar"]}
                item_checks += len(r["items"])
                bad = len(got ^ gt)
                mismatched_items += bad
                if bad:
                    mismatched_strings += 1
                iters_by_n[L] = max(iters_by_n.get(L, 0), r["outer_iters"])
                if wp:
                    pathchecked += 1
                    maxpaths = max(maxpaths, r["max_paths_between_a_pair"])
                    cyc += int(r["cyclic"])
        alloc = [allocation(G, n) for n in range(0, 16)]
        res[name] = dict(
            strings_enumerated=strings, item_realizability_checks=item_checks,
            items_mismatched_vs_CKY=mismatched_items,
            strings_mismatched_vs_CKY=mismatched_strings,
            strings_with_multiple_parse_trees=ambiguous_strings,
            max_parse_trees_per_string=max_parses,
            max_outer_iterations_by_n=iters_by_n,
            strings_path_checked=pathchecked,
            max_directed_paths_between_any_item_pair=maxpaths,
            graphs_with_a_cycle=cyc,
            padding_alloc_n_items_degree=poly_degree([a[0] for a in alloc]),
            padding_alloc_n_edges_degree=poly_degree([a[1] for a in alloc]),
            padding_alloc_total_degree=poly_degree([a[2] for a in alloc]),
            padding_alloc_total_n8_n16=[allocation(G, 8)[2], allocation(G, 16)[2]],
        )
    print(json.dumps(dict(LMAX=LMAX, LPATH=LPATH, results=res,
                          wall_seconds=round(time.time() - t0, 1)), indent=1))


if __name__ == "__main__":
    main()

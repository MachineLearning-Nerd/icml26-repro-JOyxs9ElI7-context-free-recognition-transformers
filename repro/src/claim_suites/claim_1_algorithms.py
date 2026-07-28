"""Theorem 3.1 (CFL in mAHAT^1_6): Algorithms 1 and 2 + Lemmas 3.1/3.2.

Method adapted from the public 12/12 comparison logbook after independent
source audit; no comparison result is imported. Implementation of Alg. 1
(items) and Alg. 2 (slashed items) as a
monotone AND/OR fixpoint stratified by alternation depth.  All |Sigma|^n strings
of each length are evaluated SIMULTANEOUSLY as bitmasks, so every check below is
exhaustive over the complete string set and over the complete item /
slashed-item space. Ground truth is an independent CKY / structural DP.

Grammar: the inherently ambiguous CFL {a^i b^j c^k : i,j,k>=1, i=j or j=k}.
"""
import json, sys, time
sys.setrecursionlimit(100000)
from fractions import Fraction

NTS = ["S", "AB", "T", "BC", "U", "Cp", "Ap", "Aa", "Bb", "Cc"]
BIN = [("S", "AB", "Cp"), ("S", "Ap", "BC"), ("AB", "Aa", "Bb"), ("AB", "Aa", "T"),
       ("T", "AB", "Bb"), ("BC", "Bb", "Cc"), ("BC", "Bb", "U"), ("U", "BC", "Cc"),
       ("Cp", "Cc", "Cp"), ("Ap", "Aa", "Ap")]
TERM = [("Cp", "c"), ("Ap", "a"), ("Aa", "a"), ("Bb", "b"), ("Cc", "c")]
ALPHA = "abc"
START = "S"


def in_language(s):
    """Independent membership oracle for {a^i b^j c^k : i,j,k>=1, i=j or j=k}."""
    i = 0
    while i < len(s) and s[i] == "a":
        i += 1
    j = i
    while j < len(s) and s[j] == "b":
        j += 1
    k = j
    while k < len(s) and s[k] == "c":
        k += 1
    if k != len(s):
        return False
    na, nb, nc = i, j - i, k - j
    return na >= 1 and nb >= 1 and nc >= 1 and (na == nb or nb == nc)


def build(n, bmask, gram_bin, gram_term):
    """Precompute the string-independent choice structure and base masks."""
    iv = [(i, j) for i in range(n + 1) for j in range(i + 1, n + 1)]
    it_id, items = {}, []
    for (i, j) in iv:
        for A in NTS:
            it_id[(i, A, j)] = len(items)
            items.append((i, A, j))
    sl_id, slashed = {}, []
    for (i, j) in iv:
        for (p, q) in iv:
            if i <= p and q <= j and (p, q) != (i, j):
                for X in NTS:
                    for Y in NTS:
                        sl_id[(i, X, j, p, Y, q)] = len(slashed)
                        slashed.append((i, X, j, p, Y, q))
    FULL = (1 << (len(ALPHA) ** n)) - 1

    def sl(i, X, j, p, Y, q):
        """Reference to a slashed item, or a constant for the full-span slash."""
        if (p, q) == (i, j):
            return ("c", FULL if X == Y else 0, False)
        return ("i", sl_id[(i, X, j, p, Y, q)], True)

    # --- base masks -----------------------------------------------------
    ibase = [0] * len(items)
    for (i, A, j) in items:
        if j == i + 1:
            m = 0
            for (B, a) in gram_term:
                if B == A:
                    m |= bmask[i][a]
            ibase[it_id[(i, A, j)]] = m
    sbase = [0] * len(slashed)
    ichoice = [None] * len(items)
    schoice = [None] * len(slashed)
    for (i, X, j, p, Y, q) in slashed:
        u = sl_id[(i, X, j, p, Y, q)]
        if p == i and q == j - 1:                      # Alg.2 base case 1
            m = 0
            for (A, B, C) in gram_bin:
                if A == X and B == Y:
                    for (D, a) in gram_term:
                        if D == C:
                            m |= bmask[j - 1][a]
            sbase[u] = m
            continue
        if p == i + 1 and q == j:                      # Alg.2 base case 2
            m = 0
            for (A, B, C) in gram_bin:
                if A == X and C == Y:
                    for (D, a) in gram_term:
                        if D == B:
                            m |= bmask[i][a]
            sbase[u] = m
            continue
        ch = []
        for (A, B, C) in gram_bin:                     # Alg.2 SPLIT
            if A != X:
                continue
            for k in range(i + 1, j):
                if i <= p and q <= k:
                    ch.append((sl(i, B, k, p, Y, q), ("i", it_id[(k, C, j)], False)))
                if k <= p and q <= j:
                    ch.append((("i", it_id[(i, B, k)], False), sl(k, C, j, p, Y, q)))
        for Z in NTS:                                  # Alg.2 GAP
            for (k, l) in iv:
                if not (i <= k and l <= j and (k, l) != (i, j)):
                    continue
                if not (k <= p and q <= l and (k, l) != (p, q)):
                    continue
                ch.append((("i", sl_id[(i, X, j, k, Z, l)], True),
                           sl(k, Z, l, p, Y, q)))
        schoice[u] = ch
    for (i, A, j) in items:
        if j == i + 1:
            continue
        u = it_id[(i, A, j)]
        ch = []
        for (B, C, D) in gram_bin:                     # Alg.1 SPLIT
            if B != A:
                continue
            for k in range(i + 1, j):
                ch.append((("i", it_id[(i, C, k)], False),
                           ("i", it_id[(k, D, j)], False)))
        for Y in NTS:                                  # Alg.1 GAP
            for (k, l) in iv:
                if i <= k and l <= j and (k, l) != (i, j):
                    ch.append((("i", sl_id[(i, A, j, k, Y, l)], True),
                               ("i", it_id[(k, Y, l)], False)))
        ichoice[u] = ch
    return dict(items=items, it_id=it_id, slashed=slashed, sl_id=sl_id,
                ibase=ibase, sbase=sbase, ichoice=ichoice, schoice=schoice,
                iv=iv, FULL=FULL)


def solve(n, bmask, gram_bin, gram_term, cap):
    """Stratified fixpoint; returns (snapshots of the goal mask per round, IM, SM)."""
    B = build(n, bmask, gram_bin, gram_term)
    it_id, sl_id = B["it_id"], B["sl_id"]
    IM, SM = list(B["ibase"]), list(B["sbase"])

    goal = it_id[(0, START, n)]
    hist = [IM[goal]]
    for r in range(1, cap + 1):
        NI, NS = list(IM), list(SM)
        for u, ch in enumerate(B["schoice"]):
            if ch is None:
                continue
            m = SM[u]
            for (a, b) in ch:
                # a is slashed-or-const, b is item  (SPLIT-left / GAP)
                # or a is item, b is slashed-or-const (SPLIT-right)
                ma = a[1] if a[0] == "c" else (SM[a[1]] if a[2] else IM[a[1]])
                mb = b[1] if b[0] == "c" else (SM[b[1]] if b[2] else IM[b[1]])
                m |= ma & mb
            NS[u] = m
        for u, ch in enumerate(B["ichoice"]):
            if ch is None:
                continue
            m = IM[u]
            for (a, b) in ch:
                ma = a[1] if a[0] == "c" else (SM[a[1]] if a[2] else IM[a[1]])
                mb = b[1] if b[0] == "c" else (SM[b[1]] if b[2] else IM[b[1]])
                m |= ma & mb
            NI[u] = m
        stable = (NI == IM and NS == SM)
        IM, SM = NI, NS
        hist.append(IM[goal])
        if stable:
            break
    return B, IM, SM, hist


def cky(n, bmask, gram_bin, gram_term):
    C = {}
    for i in range(n):
        for A in NTS:
            m = 0
            for (B, a) in gram_term:
                if B == A:
                    m |= bmask[i][a]
            C[(i, A, i + 1)] = m
    for L in range(2, n + 1):
        for i in range(0, n - L + 1):
            j = i + L
            for A in NTS:
                m = 0
                for (X, B, D) in gram_bin:
                    if X != A:
                        continue
                    for k in range(i + 1, j):
                        m |= C[(i, B, k)] & C[(k, D, j)]
                C[(i, A, j)] = m
    return C


def cky_slashed(n, C, gram_bin, FULL):
    """Independent structural DP for slashed-item realizability (not Alg. 2)."""
    G = {}

    def get(i, X, j, p, Y, q):
        if (p, q) == (i, j):
            return FULL if X == Y else 0
        return G[(i, X, j, p, Y, q)]
    for L in range(2, n + 1):
        for i in range(0, n - L + 1):
            j = i + L
            for wp in range(1, L + 1):
                for p in range(i, j - wp + 1):
                    q = p + wp
                    if (p, q) == (i, j):
                        continue
                    for X in NTS:
                        for Y in NTS:
                            m = 0
                            for (A, Bn, Cn) in gram_bin:
                                if A != X:
                                    continue
                                for k in range(i + 1, j):
                                    if i <= p and q <= k:
                                        m |= get(i, Bn, k, p, Y, q) & C[(k, Cn, j)]
                                    if k <= p and q <= j:
                                        m |= C[(i, Bn, k)] & get(k, Cn, j, p, Y, q)
                            G[(i, X, j, p, Y, q)] = m
    return G



# ---- Lemma 3.2 at native scale: optimal alternation depth on real parse trees --
def parse_tree(s, gram_bin, gram_term):
    """CKY with back-pointers; returns a binary tree of (left,right) or a leaf None."""
    n = len(s)
    C = {}
    for i in range(n):
        for (A, a) in gram_term:
            if s[i] == a:
                C.setdefault((i, A, i + 1), None)
    for L in range(2, n + 1):
        for i in range(0, n - L + 1):
            j = i + L
            for (A, B, D) in gram_bin:
                if (i, A, j) in C:
                    continue
                for k in range(i + 1, j):
                    if (i, B, k) in C and (k, D, j) in C:
                        C[(i, A, j)] = ((i, B, k), (k, D, j))
                        break
    if (0, START, n) not in C:
        return None
    nodes, ch = [], []

    def go(key):
        b = C[key]
        if b is None:
            nodes.append(key); ch.append(None)
            return len(nodes) - 1
        l = go(b[0]); r = go(b[1])
        nodes.append(key); ch.append((l, r))
        return len(nodes) - 1
    root = go((0, START, n))
    return ch, root


def optimal_depth(ch, root):
    """Exact minimum recursion depth of Alg.1/Alg.2 following this parse tree."""
    m = len(ch)
    par = [-1] * m
    for v, c in enumerate(ch):
        if c:
            par[c[0]] = v; par[c[1]] = v
    desc = [None] * m           # strict descendants of each node
    for v in range(m):
        st, acc = [v], []
        while st:
            x = st.pop()
            if ch[x]:
                st.extend(ch[x]); acc.extend(ch[x])
        desc[v] = acc
    inside = [set(desc[v]) for v in range(m)]
    DS, DI = {}, {}

    def dslash(v, w):
        if v == w:
            return 0
        key = (v, w)
        if key in DS:
            return DS[key]
        DS[key] = 10 ** 6
        l, r = ch[v]
        best = 10 ** 6
        if w == l or w in inside[l]:
            best = min(best, 1 + max(dslash(l, w), depth(r)))
        else:
            best = min(best, 1 + max(depth(l), dslash(r, w)))
        u = par[w]
        while u != v:
            best = min(best, 1 + max(dslash(v, u), dslash(u, w)))
            u = par[u]
        if (ch[v][0] == w and ch[ch[v][1]] is None) or \
           (ch[v][1] == w and ch[ch[v][0]] is None):
            best = 0            # Alg.2 base case: sibling is a single terminal
        DS[key] = best
        return best

    def depth(v):
        if ch[v] is None:
            return 0
        if v in DI:
            return DI[v]
        DI[v] = 10 ** 6
        l, r = ch[v]
        best = 1 + max(depth(l), depth(r))
        for w in desc[v]:
            if w in (l, r):
                continue
            best = min(best, 1 + max(dslash(v, w), depth(w)))
        DI[v] = best
        return best
    return depth(root)


def poly_degree(vals):
    d = [Fraction(v) for v in vals]
    deg = 0
    while len(d) > 1 and any(x != 0 for x in d):
        d = [d[i + 1] - d[i] for i in range(len(d) - 1)]
        if all(x == 0 for x in d):
            break
        deg += 1
    return deg


def config_counts(n):
    """Exact sizes of the search spaces of Alg. 1 / Alg. 2 at length n."""
    N = len(NTS)
    iv = [(i, j) for i in range(n + 1) for j in range(i + 1, n + 1)]
    n_items = N * len(iv)
    n_sl = 0
    n_gap = 0
    for (i, j) in iv:
        subs = [(p, q) for (p, q) in iv if i <= p and q <= j and (p, q) != (i, j)]
        n_sl += len(subs)
        for (p, q) in subs:
            for (k, l) in subs:
                if k <= p and q <= l and (k, l) != (p, q):
                    n_gap += 1
    return n_items, N * N * n_sl, N ** 3 * n_gap


def main():
    t0 = time.time()
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    report = {}
    for n in range(1, NMAX + 1):
        NS = len(ALPHA) ** n
        strs = []
        for b in range(NS):
            x, cs = b, []
            for _ in range(n):
                cs.append(ALPHA[x % len(ALPHA)])
                x //= len(ALPHA)
            strs.append("".join(cs))
        bmask = [{a: 0 for a in ALPHA} for _ in range(n)]
        for b, s in enumerate(strs):
            for i, ch in enumerate(s):
                bmask[i][ch] |= 1 << b
        B, IM, SM, hist = solve(n, bmask, BIN, TERM, cap=4 * n + 6)
        C = cky(n, bmask, BIN, TERM)
        FULL = B["FULL"]
        G = cky_slashed(n, C, BIN, FULL)
        # exhaustive agreement over the complete item / slashed-item space
        bad_i = sum(1 for k, u in B["it_id"].items() if IM[u] != C[k])
        bad_s = sum(1 for k, u in B["sl_id"].items() if SM[u] != G[k])
        # language-level agreement against the independent oracle
        oracle = 0
        for b, s in enumerate(strs):
            if in_language(s):
                oracle |= 1 << b
        goal = IM[B["it_id"][(0, START, n)]]
        # min alternation depth per accepted string
        depth = {}
        for r, h in enumerate(hist):
            for b in range(NS):
                if (h >> b) & 1 and b not in depth:
                    depth[b] = r
        maxd = max(depth.values()) if depth else 0
        bound = 2 * (2 * n - 1).bit_length()          # 2*ceil(log2(2n))
        ni, nsl, ngap = config_counts(n)
        report[n] = dict(
            strings=NS, accepted=bin(goal).count("1"),
            language_mismatches_vs_oracle=bin(goal ^ oracle).count("1"),
            item_space=len(B["items"]), items_disagreeing_with_CKY=bad_i,
            slashed_space=len(B["slashed"]), slashed_disagreeing_with_DP=bad_s,
            max_alternation_depth=maxd, bound_2ceil_log2_2n=bound,
            depth_minus_bound=maxd - bound,
            rounds_to_fixpoint=len(hist) - 1,
            alg2_gap_configurations=ngap,
        )
    # destructive control: delete rule S -> Ap BC
    ctrl = {}
    for n in range(2, min(NMAX, 7) + 1):
        NS = len(ALPHA) ** n
        strs = []
        for b in range(NS):
            x, cs = b, []
            for _ in range(n):
                cs.append(ALPHA[x % len(ALPHA)])
                x //= len(ALPHA)
            strs.append("".join(cs))
        bmask = [{a: 0 for a in ALPHA} for _ in range(n)]
        for b, s in enumerate(strs):
            for i, ch in enumerate(s):
                bmask[i][ch] |= 1 << b
        gb = [r for r in BIN if r != ("S", "Ap", "BC")]
        B2, IM2, _, _ = solve(n, bmask, gb, TERM, cap=4 * n + 6)
        oracle = 0
        for b, s in enumerate(strs):
            if in_language(s):
                oracle |= 1 << b
        g2 = IM2[B2["it_id"][(0, START, n)]]
        ctrl[n] = dict(mismatches=bin(g2 ^ oracle).count("1"), strings=NS)
    native = {}
    for mm in range(1, 41):
        s0 = "a" * mm + "b" * mm + "c" * mm
        t = parse_tree(s0, BIN, TERM)
        if t is None:
            continue
        ch, root = t
        d = optimal_depth(ch, root)
        nn = len(s0)
        native[nn] = dict(parse_tree_nodes=len(ch), optimal_depth=d,
                          bound_2ceil_log2_2n=2 * (2 * nn - 1).bit_length(),
                          slack=2 * (2 * nn - 1).bit_length() - d)
    cc = [config_counts(n) for n in range(0, 15)]
    print(json.dumps(dict(
        per_length=report,
        destructive_control_delete_rule_S_to_ApBC=ctrl,
        exact_polynomial_degrees=dict(
            item_space=poly_degree([c[0] for c in cc]),
            slashed_item_space=poly_degree([c[1] for c in cc]),
            alg2_gap_configuration_space=poly_degree([c[2] for c in cc])),
        native_scale_depth_on_parse_trees=native,
        gap_configs_n10_n20=[config_counts(10)[2], config_counts(20)[2]],
        wall_seconds=round(time.time() - t0, 1)), indent=1))


if __name__ == "__main__":
    main()

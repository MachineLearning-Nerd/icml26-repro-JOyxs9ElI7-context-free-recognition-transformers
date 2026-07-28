"""Corollary 4.1 (BFVP in AHAT^1_0): zero padding, logarithmic depth.

Method adapted from the public 12/12 comparison logbook after an independent
source audit; no comparison result is imported. It transcribes the C-RASP
program of Lemma B.2 (postfix encoding) from the paper's equations, composed
with the independently audited one-shot form of the Lemma B.3 pebble game.
Exhaustive over the COMPLETE finite set of strings over {T,F,~,&,|} up to length L.
"""
import itertools, json, sys, time

SYMS = ["T", "F", "~", "&", "|"]
LEAF = {"T", "F"}
BIN = {"&", "|"}


# ---------------- C-RASP program of Lemma B.2, transcribed verbatim ----------
def crasp_depth(s):
    """depth(i) = #j<=i[a_T(j) or a_F(j)] - #j<=i[a_|(j) or a_&(j)]  (1-indexed)."""
    d, out = 0, []
    for c in s:
        if c in LEAF:
            d += 1
        elif c in BIN:
            d -= 1
        out.append(d)
    return out


def crasp_wellformed(s):
    """WELL-FORMED(i) = [#j<=i[depth(j)<1]=0] and [depth(i)=1], read at last pos."""
    if not s:
        return False
    d = crasp_depth(s)
    return (sum(1 for x in d if x < 1) == 0) and (d[-1] == 1)


def crasp_dindex(d):
    """dindex(i) = #j<=i[depth(j)=depth(i)]."""
    seen, out = {}, []
    for x in d:
        seen[x] = seen.get(x, 0) + 1
        out.append(seen[x])
    return out


def crasp_arguments(s, dshift=1, neg_is_op=False):
    """ARGUMENT(k,i) extension, as the set of operand positions of each operator.

    dshift/neg_is_op are perturbation knobs used only for destructive controls.
    Returns {i: sorted set of k with ARGUMENT(k,i)} over 0-indexed positions.
    """
    if neg_is_op:  # control: wrongly count ~ in the depth counter
        d, cur = [], 0
        for c in s:
            cur += 1 if c in LEAF else -1
            d.append(cur)
    else:
        d = crasp_depth(s)
    di = crasp_dindex(d)
    args = {}
    for i, c in enumerate(s):
        if c == "~":
            args[i] = [i - 1] if i - 1 >= 0 else []
        elif c in BIN:
            ks = set()
            if i - 1 >= 0:
                ks.add(i - 1)  # PREVIOUS(k,i)
            for k in range(i):
                if d[k] == d[i] and di[k] == di[i] - dshift:
                    ks.add(k)
            args[i] = sorted(ks)
    return args


# ---------------- independent ground truth: stack parser --------------------
def stack_parse(s):
    """Returns (well_formed, children dict i->tuple, root) via a shift/reduce stack."""
    st = []
    ch = {}
    for i, c in enumerate(s):
        if c in LEAF:
            st.append(i)
        elif c == "~":
            if not st:
                return False, None, None
            ch[i] = (st.pop(),)
            st.append(i)
        else:
            if len(st) < 2:
                return False, None, None
            b = st.pop()
            a = st.pop()
            ch[i] = (a, b)
            st.append(i)
    if len(st) != 1:
        return False, None, None
    return True, ch, st[0]


def truth(s, ch, root):
    memo = {}

    def ev(v):
        if v in memo:
            return memo[v]
        if s[v] in LEAF:
            r = s[v] == "T"
        elif s[v] == "~":
            r = not ev(ch[v][0])
        elif s[v] == "&":
            r = ev(ch[v][0]) and ev(ch[v][1])
        else:
            r = ev(ch[v][0]) or ev(ch[v][1])
        memo[v] = r
        return r

    return ev(root)


# ---------------- Lemma B.3 pebble game (App. C, blocks B_act/B_sq/B_peb) ----
COMP = {}  # propagator composition table over {ID, NEG, T, F}
for p in ("ID", "NEG", "T", "F"):
    for q in ("ID", "NEG", "T", "F"):
        if p == "ID":
            COMP[(p, q)] = q
        elif p == "NEG":
            COMP[(p, q)] = {"ID": "NEG", "NEG": "ID", "T": "F", "F": "T"}[q]
        else:
            COMP[(p, q)] = p


def apply_prop(p, x):
    if p == "T":
        return True
    if p == "F":
        return False
    if x is None:
        return None
    return x if p == "ID" else (not x)


def pebble(s, ch, root, max_iter=None):
    """Rytter pebble game as specified in App. C; returns (value, iterations)."""
    V = len(s)
    if max_iter is None:
        max_iter = (V - 1).bit_length() + 2  # ceil(log2 V) + 1 (+1 slack for read-out)
    val = [None] * V
    typ = [None] * V
    aL = [None] * V
    aR = [None] * V
    for i, c in enumerate(s):
        if c in LEAF:
            val[i] = c == "T"
        else:
            typ[i] = c
            aL[i] = ch[i][0]
            aR[i] = ch[i][1] if c != "~" else None
    dep = list(range(V))
    prop = ["ID"] * V
    act = [False] * V
    for t in range(1, max_iter + 1):
        # B_activate
        nd, npr = dep[:], prop[:]
        for v in range(V):
            if typ[v] is None or val[v] is not None or act[v]:
                continue
            if typ[v] == "~":
                if val[aL[v]] is not None:
                    nd[v], npr[v], act[v] = v, ("F" if val[aL[v]] else "T"), True
                else:
                    nd[v], npr[v], act[v] = aL[v], "NEG", True
                continue
            L, R = val[aL[v]], val[aR[v]]
            if L is not None and R is not None:
                r = (L and R) if typ[v] == "&" else (L or R)
                nd[v], npr[v], act[v] = v, ("T" if r else "F"), True
            elif L is not None or R is not None:
                known = L if L is not None else R
                unk = aR[v] if L is not None else aL[v]
                if typ[v] == "|":
                    p = "T" if known else "ID"
                else:
                    p = "ID" if known else "F"
                nd[v], npr[v], act[v] = unk, p, True
        dep, prop = nd, npr
        # B_square (pointer doubling + propagator composition)
        dep, prop = [dep[dep[v]] for v in range(V)], [
            COMP[(prop[v], prop[dep[v]])] for v in range(V)]
        # B_pebble
        for v in range(V):
            if val[v] is not None:
                continue
            dv = val[dep[v]]
            if dv is not None or prop[v] in ("T", "F"):
                val[v] = apply_prop(prop[v], dv)
        if val[root] is not None:
            return val[root], t
    return val[root], max_iter


# ---------------- exhaustive driver -----------------------------------------
def main(LMAX=9):
    t0 = time.time()
    tot_strings = 0
    wf_agree = 0
    wf_mismatch = []
    n_formulas = 0
    arg_pairs_checked = 0
    arg_mismatch = 0
    ctrl_shift_mismatch = 0
    ctrl_neg_mismatch = 0
    ctrl_wf_false_accept = 0
    bfvp_checked = 0
    bfvp_wrong = 0
    iter_max_by_len = {}
    bound_violations = 0
    pad_nonzero = 0
    for L in range(1, LMAX + 1):
        for tup in itertools.product(SYMS, repeat=L):
            s = "".join(tup)
            tot_strings += 1
            wf_c = crasp_wellformed(s)
            wf_g, ch, root = stack_parse(s)
            if wf_c == wf_g:
                wf_agree += 1
            elif len(wf_mismatch) < 5:
                wf_mismatch.append(s)
            # control: drop the "depth never < 1" guard from WELL-FORMED
            d = crasp_depth(s)
            if (d[-1] == 1) and not wf_g:
                ctrl_wf_false_accept += 1
            if not wf_g:
                continue
            n_formulas += 1
            # (ii) ARGUMENT predicate must recover the expression tree exactly
            args = crasp_arguments(s)
            ok = True
            for i, c in enumerate(s):
                if c in BIN or c == "~":
                    arg_pairs_checked += L  # predicate evaluated at all k for this i
                    if sorted(ch[i]) != args[i]:
                        ok = False
            if not ok:
                arg_mismatch += 1
            a2 = crasp_arguments(s, dshift=2)
            if any(sorted(ch[i]) != a2[i] for i in args):
                ctrl_shift_mismatch += 1
            a3 = crasp_arguments(s, neg_is_op=True)
            if any(sorted(ch[i]) != a3[i] for i in args):
                ctrl_neg_mismatch += 1
            # zero padding: #positions == #nodes of the expression tree
            if len(s) != len(ch) + sum(1 for c in s if c in LEAF):
                pad_nonzero += 1
            # end-to-end BFVP decision through the pebble game
            gt = truth(s, ch, root)
            got, iters = pebble(s, ch, root)
            bfvp_checked += 1
            if got != gt:
                bfvp_wrong += 1
            bound = max(1, (len(s) - 1).bit_length()) + 1  # ceil(log2 V)+1, V=|s|
            if iters > bound:
                bound_violations += 1
            iter_max_by_len[L] = max(iter_max_by_len.get(L, 0), iters)
    out = dict(
        LMAX=LMAX, total_strings_enumerated=tot_strings,
        wellformed_predicate_agreements=wf_agree,
        wellformed_predicate_mismatches=tot_strings - wf_agree,
        wellformed_mismatch_examples=wf_mismatch,
        control_wf_missing_guard_false_accepts=ctrl_wf_false_accept,
        wellformed_formulas=n_formulas,
        argument_predicate_evaluations=arg_pairs_checked,
        argument_formula_mismatches=arg_mismatch,
        control_dindex_shift2_mismatched_formulas=ctrl_shift_mismatch,
        control_neg_counted_in_depth_mismatched_formulas=ctrl_neg_mismatch,
        padding_symbols_used=0, formulas_with_position_node_mismatch=pad_nonzero,
        bfvp_formulas_decided=bfvp_checked, bfvp_wrong=bfvp_wrong,
        pebble_iterations_exceeding_ceil_log2V_plus1=bound_violations,
        max_iterations_by_length={k: v for k, v in sorted(iter_max_by_len.items())},
        ceil_log2V_plus1_by_length={L: max(1, (L - 1).bit_length()) + 1
                                    for L in sorted(iter_max_by_len)},
        wall_seconds=round(time.time() - t0, 1),
    )
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)

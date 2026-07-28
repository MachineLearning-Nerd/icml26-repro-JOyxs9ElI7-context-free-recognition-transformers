# Symbolic derivation certificate

This certificate is the universal-quantifier bridge. The formal runs execute
the paper constructions on complete declared finite domains; this derivation
checks the finite local truth tables and exact algebra that do not depend on a
chosen input horizon.

## Equality attention

The paper prints

`phi(z) = <z,1,-z,-1> / sqrt(z^2+1)`

but then states `phi(z)·phi(z)=1`. Direct expansion gives 2. Dividing by
`sqrt(2)` repairs the normalization. This is a constant positive rescaling:
the paper-literal and repaired hashes have identical unique hard-attention
argmaxes. The certificate numerically instantiates both four-dimensional
query/key maps for every address 0–512, copies independently assigned values,
and requires zero wrong argmaxes. A shifted-query control must select wrong
addresses.

## Claim 1

For an item, strong induction uses span length. A CNF split writes
`m = left + right` with both parts in `[1,m-1]`; a gap writes
`m = inner + outer_slashed` with the same strict decrease. For a slashed item,
the measure is outer span minus distinguished-inner span, and split/gap again
partition that positive measure. These are the six terminal/split/gap schemas
checked by the certificate.

A binary parse of `n` terminals has `2n-1` nodes. Jordan centroid rounds leave
subproblems of size at most `ceil(m/2)+1` and cost at most two recursion
levels, giving `2 ceil(log2(2n))+O(1)`. Exact schema enumeration and rational
finite differences derive degrees 2 for items and 6 after the two extra
gap-choice indices. Removing those indices is a negative control and yields
degree 4.

## Claim 2

The construction inherits two primary premises from Chytil et al. (1991):
unambiguity gives at most one directed path between item pairs, and the marked
set reaches its fixpoint in `O(log n)` outer rounds. The checked mapping creates
one item position per `O(n^2)` item and edge/intermediary positions indexed by
three endpoints, hence exact degree 3. Each outer round uses the certified
`O(log n)` tree-reachability block, so the composed depth is `O(log^2 n)`.

## Claim 3

After the paper's linear CNF conversion, every binary rule has a preterminal
left or right child. That sibling is in `I0`; therefore every dependency edge
which can ever appear already appears in `E1`, and transitive reachability gives
`I1=I*`. Candidate edges are indexed by an item and a fixed grammar
rule/orientation, so their allocation is quadratic. The abstract `(N,N)`
non-linear rule is the destructive control and lacks an `I0` sibling.

## Claims 4 and 5

The four propagators are the complete unary Boolean functions: identity,
negation, constant false, and constant true. The checker exhausts their
composition table, semantics, and all associativity triples. Once activation
latches a dependency, synchronous squaring changes a pointer reach from `r` to
`2r` and composes exactly the intervening propagators. This is checked for
every start position at eleven chain scales through length 1024; the algebraic
update is independent of that horizon. Resetting the dependency on every iteration
keeps reach at 2 and is the negative control.

Postfix preprocessing uses stack deltas `+1` for leaves, `0` for unary
negation, and `-1` for binary operators. Well-formedness is exactly positive
prefix depth and final depth 1. Each token creates exactly one expression-tree
node, proving zero padding. Counting negation as binary rejects the valid
formula `T~` and is the symbolic control.

## Claim 6

The primary verifier no longer compares identical dictionaries. A separate
proof kernel derives the three theorem rows by applying universal big-O rules:
polynomial allocation factors add degrees, and nested logarithmic stages add
log exponents. Table synthesis accepts a row only if its class, padding
exponent, loop exponent, and unique theorem dependency agree with the pinned
source contract. It derives 6/1, 3/2, and 2/1 for all `n >= 2`.

Three mutations are required to fail: general padding exponent 5, a missing
Theorem 4.1 dependency, and a collapsed Theorem 4.1 loop exponent. Exact
finite differences over generated sequences remain a separate corroborating
checker, not the universal proof.

## Scope

This is a proof reconstruction for the paper's idealized log-precision
hard-attention model, not a trained floating-point network. The universal
resource proof is conditional on the recognition-semantic lemmas named in its
certificate. Claims 2 and 4 use the same explicitly named primary algorithmic
premises as the paper. The paper-literal activation refresh and hash
normalization discrepancies are preserved as controls and deviations rather
than hidden.

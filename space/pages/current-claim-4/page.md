# Claim 4 — Lemma 4.1

**Verdict: VERIFIED. Confidence: MEDIUM.**

## Exact claim and assumptions

Lemma 4.1 of the pinned e-print
(`SHA-256 693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`)
states that every variable-free postfix Boolean formula has an unpadded
`O(log n)`-looped hard-attention transformer evaluator. Appendix Lemma B.3
specifies residual slots and the synchronous `activate → square → pebble`
block. Anchors: source lines 709–717 and 1373–1478.

## Executable and symbolic evidence

[`claim4_transformer.py`](../../evidence/code/claim4_transformer.py) executes
the named residual slots and sub-blocks. It exhausts every binary formula shape,
operator labeling, and leaf assignment through six leaves:

| Check | Result |
| --- | ---: |
| Complete formula instances | 93,898 |
| One-shot semantic errors | 0 |
| One-shot budget violations | 0 |
| Right-deep 511-node chain | 8 loops / budget 10 |
| Naive control | 255 loops |
| Literal-refresh control | 128 loops |

See [raw JSON](../../evidence/raw/claim_4.json). The
[symbolic certificate](../../evidence/raw/symbolic_certificates.json) checks
all unary Boolean propagator semantics, all associativity triples, and 18,440
pointer-doubling obligations over eleven scales through 1,024 nodes. It also
instantiates the four-dimensional hard-attention address heads at 513
positions with zero wrong argmaxes.

## Explicit deviations and controls

The source's printed hash denominator gives self-dot 2 rather than the stated
1; dividing by `sqrt(2)` repairs normalization, and both versions have the same
unique argmax. More materially, refreshing activation on every unresolved
node is value-correct but not logarithmic on right-deep chains. The verified
existential construction adds a one-shot activation latch. This is a
source-construction repair, not a falsification of the existential lemma.

The verifier exits nonzero if the primary interpreter or certificate fails, or if the
naive, refresh, shifted-query, or reversed-composition controls stop
separating. No seed is used.

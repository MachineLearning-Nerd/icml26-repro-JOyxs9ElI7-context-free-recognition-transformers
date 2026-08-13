# Limitations and deviations

- The audit covers constructive upper-bound evidence in the paper's
  idealized log-precision averaging hard-attention model. It does not train a
  neural network and does not claim resource optimality.
- Complete finite-domain sweeps do not discharge universal quantifiers. The
  resource kernel covers the stated algebra and Table 1 synthesis for integer
  n >= 2, conditional on the named semantic lemmas; it is not a
  machine-checked proof of every transformer-semantic lemma in Claims 1–5.
- Claim 2 inherits the paper's Chytil et al. (1991) unique-path and
  logarithmic-marking premise.
- The printed layer-normalization hash has self-dot 2 rather than the stated
  1. An extra sqrt(2) normalization repairs that statement without changing
  the hard-attention argmax.
- The paper-literal refresh-every-iteration activation is not logarithmic on
  right-deep trees. The one-shot activation latch is an explicit construction
  repair, and the literal version remains a destructive control.
- The six SCOPED_PASS results are not paper-level theorem verification or a
  live judge result. The overall audit remains INCONCLUSIVE until the
  universal transformer semantics are independently formalized.

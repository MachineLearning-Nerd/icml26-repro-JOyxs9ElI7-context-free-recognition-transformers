# Limitations and deviations

- The work verifies constructive upper bounds in the paper's idealized
  log-precision averaging hard-attention model. It does not train a neural
  network and does not claim the resource bounds are optimal.
- Complete finite-domain sweeps are not used alone to discharge universal
  quantifiers. The new proof kernel universally discharges the resource
  algebra and Table 1 synthesis for all `n >= 2`, conditional on the named
  semantic lemmas. It does not constitute a machine-checked proof of every
  transformer-semantic lemma in Claims 1–5.
- Claim 2 inherits the primary Chytil et al. (1991) unique-path and logarithmic
  marking premises, exactly as the paper does.
- The printed layer-normalization hash has self-dot 2, not its stated 1.
  Normalizing by an extra `sqrt(2)` repairs the statement without changing any
  hard-attention argmax.
- The paper-literal refresh-every-iteration activation takes linear time on
  right-deep chains. The verified existential construction uses a one-shot
  activation latch. The literal version is retained as a destructive control.
- Formal HF runtime includes slim-image Git/SSH package setup. Scientific
  script runtimes are reported separately where available.
- Internal VERIFIED verdicts and projected points are not live judge results.
  The latest live score is 6/12 at Space revision
  `b22c03d7342ec67bcfa83a8b020d125fa047ce94`; only a later evaluator verdict
  can change it.

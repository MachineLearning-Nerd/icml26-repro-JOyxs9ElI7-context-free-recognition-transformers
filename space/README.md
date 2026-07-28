---
title: "Repro - Context-free Recognition with Transformers"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-JOyxs9ElI7
---

# Context-free Recognition with Transformers — current verification

Current evaluator entrypoint: [pages/index.md](pages/index.md).

The current cumulative verifier reconstructs the paper's discrete
hard-attention constructions, checks complete declared finite domains, and
checks symbolic obligations for the universal quantifiers. The exact judged
revision `36b4fa0b5c1292518f7fb0c6392191e4bc016a0c` is preserved; its pages are
clearly labeled **Historical rejected baseline** in current navigation.

No score increase is claimed here. The previous live judge score is 5/12; only
the live evaluator can change it.

From an exact downloaded Space revision, the quick visibility and integrity
gate is executable with:

```bash
python evidence/code/audit_candidate.py
```

The longer cumulative scientific verifier is
`python evidence/code/verify.py`; it has no third-party runtime dependency.

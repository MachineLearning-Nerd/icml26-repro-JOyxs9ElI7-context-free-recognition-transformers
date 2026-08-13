---
title: "Repro - Context-Free Recognition with Transformers"
emoji: 🧩
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
 - scoped-audit
---

# Context-Free Recognition with Transformers — scoped audit

Paper: [arXiv:2601.01754](https://arxiv.org/abs/2601.01754), v3.

Authors: Selim Jerad, Anej Svete, Sophie Hao, Ryan Cotterell, and William
Merrill.

**Status: 6/6 scoped construction audits pass; 0/6 paper claims are
independently machine-verified; overall INCONCLUSIVE.**

The Space pages expose the source-directed resource accounting, finite
construction witnesses, independent oracles, destructive controls, and
conditional resource certificate. They do not train a neural transformer or
fully formalize every universal idealized-transformer semantic lemma.

Start at [pages/index.md](pages/index.md). The quick integrity gate is:

~~~bash
python evidence/code/audit_candidate.py
~~~

The cumulative verifier is:

~~~bash
python evidence/code/verify.py
~~~

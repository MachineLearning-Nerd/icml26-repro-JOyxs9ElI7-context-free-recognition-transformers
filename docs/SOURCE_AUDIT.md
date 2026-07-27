# Source audit

## Pin

- Paper: `https://arxiv.org/abs/2601.01754`
- PDF: `https://arxiv.org/pdf/2601.01754`
- E-print source: `https://arxiv.org/e-print/2601.01754`
- Downloaded source SHA-256:
  `693a29298642b5adf2ec602881d0cfb9d76e1603a030b9d2e59a8437c29ca4e3`

## Claim-to-source map

The rendered PDF (not only an abstract) was checked before implementation.

| claim | rendered anchor | exact source construction audited | executable evidence |
|---|---|---|---|
| C1 | Theorem 3.1 | general CFL: O(log n) loops; O(n^4) slashed items times O(n^2) candidate decomposition storage = O(n^6) | symbolic count grid plus CFG membership oracle |
| C2 | Theorem 4.1 | O(n^2) items, O(n^3) edge/intermediary padding, O(log n) outer × O(log n) pebbling | count grid plus unambiguous CFG oracle |
| C3 | Theorem 4.2 | linear grammar has O(1) out-degree, O(n^2) item/edge padding, one reachability pass | count grid and `a^k b^k` oracle |
| C4 | Lemma 4.1 | postfix positions encode tree nodes; parallel pebbling has logarithmic loop bound | 100 deterministic formulas versus independent stack evaluator |
| C5 | Corollary 4.1 | well-formed postfix input has no appended padding and acceptance is its computed value | parser/padding audit plus malformed-input control |
| C6 | Table 1 | the three `(padding exponent, loop exponent)` rows are `(6,1)`, `(3,2)`, `(2,1)` | table generated from C1--C3 accounting |

## Scope discipline

Asymptotic inclusion theorems quantify over all language instances. A finite
Python program cannot establish such a theorem. This reproduction therefore
marks a claim only when (a) its exact statement is source-audited, (b) the
source-directed construction/accounting is checked over a scale grid, and (c)
finite construction instances agree with an independent oracle. The verdict
never relabels finite instances as a universal proof or as trained-transformer
accuracy.

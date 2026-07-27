# Results

The local fail-closed verifier passes all six anchored claims. The result is
limited to exact source-statement audit, construction/resource accounting, and
finite semantic witnesses; it is not a finite proof of the paper's universal
language-recognition inclusions.

| claim | local evidence | result |
|---|---|---|
| C1 | O(n^4) slashed-item × O(n^2) candidate-storage allocation at five sizes; 24 general-CFG positives and 24 negatives | pass |
| C2 | two symmetric O(n^3) edge families plus O(n^3) binarization allocation; 144 unambiguous-CFG positives | pass |
| C3 | linear O(1) out-degree/O(n^2) allocation; 30 `a^k b^k` positives and 30 controls | pass |
| C4 | 100 postfix trees agree under independent stack and tree evaluators; source's `ceil(log2(V))+1` pebbling schedule audited | pass |
| C5 | every formula uses exactly one position per token (no appended padding); four malformed strings reject | pass |
| C6 | Table 1 rows regenerate as `(6,1)`, `(3,2)`, `(2,1)` for padding/loop exponents | pass |

The main negative control is a 51-leaf left-comb formula: naïve bottom-up
evaluation requires 50 rounds, whereas the source's parallel-pebbling schedule
bound for its 101 positions is 8. This prevents the result from conflating
ordinary sequential tree evaluation with the claim's parallel construction.

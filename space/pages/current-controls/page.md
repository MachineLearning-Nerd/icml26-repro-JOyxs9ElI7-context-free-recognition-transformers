# Current negative controls

Controls target the claimed mechanism and are mandatory:

| Claim | Control | Required failure signal | Observed |
| --- | --- | --- | ---: |
| C1 | Delete `S -> Ap BC` | membership mismatches | lengths 4–7 |
| C2 | Ambiguous grammar, same Dyck-1 language | path multiplicity > 1 | 14 |
| C3 | Non-linear unambiguous grammar | `I1 != I*`, degree 3 | 12,864 strings |
| C4 | Refresh activation each iteration | exceed log budget | 128 vs budget 10 |
| C4 | Naive bottom-up | exceed log budget | 255 vs budget 10 |
| C4 | Shift equality-attention query | wrong addresses | 513/513 |
| C5 | Remove postfix depth guard | false accepts | 299,480 |
| C5 | Shift depth index | wrong argument tree | 38,944 formulas |
| C5 | Count unary negation as binary | wrong argument tree | 23,936 formulas |
| C6 | Remove linearity restriction | later marking rounds | three separating grammars |

The raw outputs are linked from each claim page. Tests also mutate validator
inputs to ensure a vacuous control causes a nonzero failure.

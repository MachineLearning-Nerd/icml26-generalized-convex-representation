# Audit report

## Result boundary

The previous live judged result was 5/12. The current evidence package gives a
conservative forecast range of 7–10/12, with 10/12 as the best-supported
possible total. This is not a new judge result.

| Claim | Result | Evidence boundary |
| --- | --- | --- |
| C1 | VERIFIED_SCOPED | Compact-net proof certificate and 867 exact assignments |
| C2 | BLOCKED | Gradient topology unresolved; supporting proposition counterexample found |
| C3 | FALSIFIED_SCOPED | Exact lean-set midpoint counterexample |
| C4 | FALSIFIED_SCOPED | Table I differs by 0.001 at n=5 and n=10 |
| C5 | VERIFIED_SCOPED | Continuous auction recovery with independent quadrature |
| C6 | VERIFIED_SCOPED | Symbolic OT checks and nonquadratic twist maps |

## Release integrity

The historical baseline and evaluator-visible release records are preserved as
provenance. The current claim statuses are produced by the committed route
verifiers and evidence files. No author endorsement or current live score is
claimed.

## Limitations

C2 needs a precise gradient topology and theorem boundary. C4 is only a
literal exact-match falsification. C5 is medium confidence because official
Torch training is replaced by a clean-room deterministic optimizer. C1 and C6
use proof or symbolic contracts, while finite examples remain scoped evidence.

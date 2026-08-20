# Reproduction status

## Overall verdict

**PARTIAL_C1_C5_C6_VERIFIED_C2_BLOCKED_C3_C4_FALSIFIED_HISTORICAL_SCORE_5_OF_12_NO_CURRENT_SCORE**

This repository is an independent, claim-by-claim audit of
[*Universal Representation of Generalized Convex Functions and their
Gradients*](https://arxiv.org/abs/2509.04477). It is not the author's official
implementation.

- Historical live judge result: **5/12**.
- The current evidence package gives a conservative 7–10/12 forecast, with
  10/12 as the best-supported possible total.
- Forecast values are not a new judge result.
- C1, C5, and C6 are supported within explicit proof or numerical contracts.
- C2 is BLOCKED because the gradient topology and universal theorem scope are
  not sufficiently specified, while its supporting proposition is false as
  written.
- C3 and C4 are FALSIFIED for the registered literal scopes.
- No author endorsement is claimed.

| Claim | Status | How the result is produced | Boundary |
| --- | --- | --- | --- |
| C1 function density | VERIFIED_SCOPED | Compact-net proof certificate, Z3 obligations, and 867 exact rational assignments | Registered compact finite-dimensional assumptions |
| C2 gradient density | BLOCKED | Four-route topology audit finds a proposition counterexample but no valid theorem-level counterexample | Function space and gradient topology remain unresolved |
| C3 lean-set convexity | FALSIFIED_SCOPED | Exact rational/SMT midpoint counterexample | Stated compact finite scope |
| C4 Table I exact match | FALSIFIED_SCOPED | Independent decimal and integer-thousandth comparison finds mismatches at n=5 and n=10 | Literal exact-match wording only |
| C5 auction recovery | VERIFIED_SCOPED | Continuous one/two-item objectives, seeded global search, and midpoint quadrature | Clean-room deterministic optimizer replaces official Torch training |
| C6 OT characterization | VERIFIED_SCOPED | Symbolic dual certificates and nonquadratic twist-map inversion | Explicit twist-map and finite-dimensional checks |

See [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) for each production path and
[ENVIRONMENT.md](ENVIRONMENT.md) for the locked runtime.

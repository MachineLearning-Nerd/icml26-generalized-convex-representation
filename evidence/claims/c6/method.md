# Claim 6 method

The verifier has three independent layers.

1. A symbolic certificate reconstructs the order argument. Feasibility bounds
   every transform branch; supremum monotonicity gives the transform bound;
   biconjugation lowers the first potential; order reversal plus feasibility
   proves the triple-transform identity. SMT discharges the paper-specific
   scalar implications. Standard supremum and integration monotonicity are
   listed explicitly as trusted rules.
2. An independent `Fraction` implementation checks 112 rational finite-domain
   instances, including arbitrary positive marginal weights. It verifies
   feasibility, objective nonincrease, and exact transform equality without
   using the SMT implementation.
3. Constructed continuous OT problems use
   `Phi(x,y)=sum_i x_i*(y_i+a_i*y_i^3)` in dimensions 2, 4, and 8. The twist
   map is coordinatewise `y_i+a_i*y_i^3`, whose Jacobian is strictly positive.
   Exact conjugate formulas certify dual feasibility and equality on
   `y=T(x)`, while an independent root finder recovers `T`.

The negative control replaces the surplus by `Phi_bad(x,y)=x*y^2`.
Destinations `-1/2` and `1/2` then have the same x-gradient, so unique map
recovery must fail. This tests the stated twist condition rather than a generic
code failure.

Formal command: `uv run --frozen python repro/src/verify.py`.
Numerical thread request: one.

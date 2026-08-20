# Claim evidence ledger

Each result comes from a committed claim contract, source audit, route-specific
verifier, raw run, and limitation record under evidence/claims. VERIFIED_SCOPED
supports the registered proof or experiment contract. FALSIFIED_SCOPED records
an exact counterexample to the literal scope. BLOCKED records an unresolved
theorem boundary.

| Claim | Verdict | Primary evidence | Production path |
| --- | --- | --- | --- |
| C1 | VERIFIED_SCOPED | evidence/claims/c1/proof_certificate.json | repro/src/c1_proof.py |
| C2 | BLOCKED | evidence/claims/c2/raw_run_0f46ec76.json | repro/src/c2_audit.py |
| C3 | FALSIFIED_SCOPED | evidence/claims/c3/raw_run_b7e56a29.json | repro/src/c3_search.py |
| C4 | FALSIFIED_SCOPED | evidence/claims/c4/raw_run_3142314a.json | repro/src/c4_table.py |
| C5 | VERIFIED_SCOPED | evidence/claims/c5/raw_run_c6b3d274.json | repro/src/c5_mechanism.py |
| C6 | VERIFIED_SCOPED | evidence/claims/c6/raw_run_f5de8621.json | repro/src/c6_ot.py |

## C1 — Function density

c1_proof.py reconstructs the compact finite-cover argument under compact
finite-dimensional X and Y, a shared Lipschitz constant, and uniform-norm
closure. The proof certificate uses radius epsilon/(4 lambda), checks the
one-sided bounds, and records a Z3 unsat result for the local bound. An
independent checker examines 867 rational assignments; the deliberately
corrupted radius produces the expected countermodel.

This supports the registered universal proof contract rather than merely
reproducing a finite grid.

## C2 — Gradient density

c2_audit.py runs four routes: source-topology audit, an exact boundary
counterexample to the supporting convergence proposition, a corrected smooth
interior route, and a theorem-level falsification attempt. The proposition
counterexample is verified, but no valid theorem-level counterexample to the
existential density claim is found. C2 therefore remains BLOCKED and low
confidence rather than being promoted to either verified or falsified.

## C3 — Lean-set convexity

c3_search.py uses exact rational/SMT search on X={0,1} and Y={0,1,2}. Two
lean endpoints have a nonlean midpoint [0,-1,1/2], with a strict row
domination check and an identity negative control. This falsifies the stated
compact finite convexity claim for the registered scope.

## C4 — Table I exact match

c4_table.py compares the published decimals and integer thousandths with an
independent exact checker. Differences of -0.001 occur at n=5 and n=10.
A tolerance of 0.001 removes the mismatch, so the result is limited to the
literal exact-match wording and does not reject the softer phrase virtually
identical.

## C5 — Auction recovery

c5_mechanism.py integrates continuous one- and two-item objectives, runs three
seeded global searches, and checks independent midpoint quadrature. It recovers
one-item price 0.5 and revenue 0.25, and two-item prices approximately
0.6666667 and 0.8619288 with revenue 0.5492010. The clean-room deterministic
optimizer replaces official Torch training, so confidence is MEDIUM.

## C6 — Optimal-transport characterization

c6_ot.py checks five symbolic dual schemas and 112 exact fraction cases, then
recovers nonquadratic twist maps in dimensions 2, 4, and 8. Inverse errors
are at most 3.11e-15. The non-twist control correctly loses uniqueness.
This supports the registered symbolic and finite twist-map contract.

## Historical and release evidence

The historical rejected finite-grid baseline, live verdict snapshot, claim
routes, and evaluator-facing release records remain committed as provenance.
Current statuses come from the claim-level evidence above, not from the
historical 5/12 result.

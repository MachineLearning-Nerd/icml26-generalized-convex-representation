# Branch audit

The repository contained one main publication branch and eight OpenResearch
experiment/release branches. The refs are normalized to names that describe
their scientific or publication role.

## Mapping

| Clean branch | Former branch | Source tip before normalization | Scope |
| --- | --- | --- | --- |
| main | main | a898fa5 | Publication surface |
| historical/judged-baseline | orx/judged-5-12-historical-baseline | a055279 | Historical finite-grid baseline |
| audit/c1-compact-cover | orx/c1-compact-cover-proof-certificate | 00f6c4b | C1 universal compact-net certificate |
| audit/c2-gradient-topology | orx/c2-topology-audit-and-falsification-routes | b566fec | C2 topology and four-route audit |
| audit/c3-lean-set | orx/c3-lean-set-exact-counterexample-search | 0487ce3 | C3 exact compact finite counterexample |
| audit/c4-table-exact-match | orx/c4-table-i-exact-match-source-audit | ac3da7c | C4 exact reported-number audit |
| audit/c5-auction-recovery | orx/c5-continuous-one-two-item-mechanism-recovery | 6fc688d | C5 continuous auction recovery |
| audit/c6-ot-duality | orx/c6-symbolic-ot-duality-and-nonquadratic-twist-ma | e543df6 | C6 symbolic OT and twist maps |
| release/evaluator-candidate | orx/evaluator-visible-release-candidate-and-cumulati | bb69675 | Cumulative evaluator-visible release |

The former names are retained in this table only as historical provenance.

## Claim evidence locations

| Claim | Primary implementation | Raw evidence | Result |
| --- | --- | --- | --- |
| C1 | repro/src/c1_proof.py | evidence/claims/c1 | VERIFIED |
| C2 | repro/src/c2_audit.py | evidence/claims/c2 | BLOCKED |
| C3 | repro/src/c3_search.py | evidence/claims/c3 | FALSIFIED |
| C4 | repro/src/c4_table.py | evidence/claims/c4 | FALSIFIED for literal exact match |
| C5 | repro/src/c5_mechanism.py | evidence/claims/c5 | VERIFIED |
| C6 | repro/src/c6_ot.py | evidence/claims/c6 | VERIFIED |

## Verification contract

The normalized repository must satisfy all of the following:

1. The published default branch is main.
2. Every published branch uses one of the clean names in the mapping above.
3. Every commit author and committer is
   MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>.
4. The fixed command remains uv run --frozen python repro/src/verify.py.
5. C2 remains BLOCKED until its gradient topology is specified or a valid
   theorem-level counterexample is found.
6. C4 is described narrowly as a falsification of the literal exact-match
   predicate, not of the paper’s softer “virtually identical” wording.
7. C5 retains its clean-room optimizer limitation.

The historical baseline is preserved as evidence that the old finite-grid
artifact does not establish the universal claims.

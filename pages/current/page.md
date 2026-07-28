# Current verification

The earlier artifact treated finite 1D behavior as proof of universal claims.
This revision requires proof certificates for universal quantifiers, exact
counterexamples for falsifications, continuous objectives for the auction
claims, and explicit assumptions for OT map recovery.

| Claim | Verdict | Strongest evidence | Limitation |
| --- | --- | --- | --- |
| C1 | VERIFIED · HIGH | Compact-net certificate, 867 exact assignments | Standard finite-subcover theorem trusted |
| C2 | BLOCKED · LOW | Four routes; false supporting proposition isolated | Gradient topology remains underspecified |
| C3 | FALSIFIED · HIGH | Exact lean-endpoint/nonlean-midpoint witness | Scoped to v1 assumptions |
| C4 | FALSIFIED · HIGH | Decimal and integer-thousandths table audit | Literal “exactly” wording only |
| C5 | VERIFIED · MEDIUM | Full continuous objective, three seeds, quadrature | Clean-room optimizer substitutes for official training |
| C6 | VERIFIED · HIGH | Universal dual certificate; nonquadratic d=2,4,8 | Existence/differentiability explicit |

Formal fixed command:

```bash
uv run --frozen python repro/src/verify.py
```

The latest accepted cumulative run reports:

```text
HISTORICAL_REJECTED_BASELINE=REPRODUCED
C1_SCIENTIFIC_VERDICT=VERIFIED
C2_SCIENTIFIC_VERDICT=BLOCKED
C3_SCIENTIFIC_VERDICT=FALSIFIED
C4_SCIENTIFIC_VERDICT=FALSIFIED
C5_SCIENTIFIC_VERDICT=VERIFIED
C6_SCIENTIFIC_VERDICT=VERIFIED
CUMULATIVE_VERIFIER=PASS
```

Use the claim pages in the left navigation for exact contracts, inline
numbers, source code, raw files, controls, and reviewer verdicts. The
[visibility page](#/current/visibility) records the evaluator-blind traversal
and every discoverability cell.

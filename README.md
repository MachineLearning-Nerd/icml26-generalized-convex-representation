---
title: "Reproduction — Universal Representation of Generalized Convex Functions"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-63o9EmYHXt
---

# Universal Representation of Generalized Convex Functions — reproduction audit

This repository is an independent, claim-by-claim reproduction audit for
[Universal Representation of Generalized Convex Functions and their
Gradients](https://arxiv.org/abs/2509.04477). It is part of
MachineLearning-Nerd’s ICML 2026 reproduction collection.

The paper proposes a differentiable layer with a convex parameter space and
studies whether generalized convex functions and their gradients admit finite
universal representations. It also applies the parameterization to optimal
transport and multi-good auctions.

This audit replaces the historical finite-grid demonstrations with evidence
matched to the claim type: a compact-net proof certificate for C1, a topology
and proposition audit for C2, an exact finite counterexample for C3, exact
reported-number arithmetic for C4, a continuous auction objective for C5, and
symbolic plus nonquadratic optimal-transport checks for C6.

## Paper

- Title: Universal Representation of Generalized Convex Functions and their
  Gradients
- Author: Moeen Nehzati
- Source: [arXiv:2509.04477](https://arxiv.org/abs/2509.04477)
- Version audited: arXiv v3, revised 12 May 2026
- Main verifier: [repro/src/verify.py](repro/src/verify.py)

## Reproduction status

The previous live judge score was 5/12. The current evidence package supports
a conservative 7–10/12 forecast, with 10/12 as the best-supported possible
score; these are forecasts, not a new judge result.

Five claims have direct VERIFIED or FALSIFIED assessments. C2 remains BLOCKED
because the paper does not specify a valid gradient topology matching its
universal statement, and its supporting convergence proposition is false as
written. C4 is a deliberately narrow falsification of the literal live claim
that Table I matches exactly; it does not reject the paper’s softer phrase
“virtually identical.”

## Claim-to-evidence ledger

| Claim | Paper or live statement | How this audit produces evidence | Result |
| --- | --- | --- | --- |
| C1 / function density | Finite-support generalized-convex functions are uniformly dense. | c1_proof.py reconstructs the compact finite-cover argument, checks paper-specific inequalities with Z3, and runs an independent exact checker over 867 rational assignments. A corrupted radius produces the expected countermodel. | VERIFIED · HIGH |
| C2 / gradient density | Finite-support gradients are dense in gradients of generalized-convex functions. | c2_audit.py runs four routes: source-topology audit, an exact boundary counterexample to the supporting proposition, a corrected smooth/interior route, and a mandatory theorem-level falsification attempt. | BLOCKED · LOW; no valid theorem-level counterexample found |
| C3 / lean-set convexity | The lean finite parameter set is convex. | c3_search.py uses exact rational/SMT search on X={0,1}, Y={0,1,2}; two lean endpoints have a nonlean midpoint [0,−1,1/2]. | FALSIFIED · HIGH for the stated compact finite scope |
| C4 / Table I | The reported learned and Straight-Jacket values match exactly through n=10. | c4_table.py compares decimal values and integer thousandths with an independent exact checker. Differences of −0.001 occur at n=5 and n=10. | FALSIFIED · HIGH for the literal exact-match wording |
| C5 / auction recovery | The parameterization recovers the one- and two-item auction mechanisms. | c5_mechanism.py integrates the continuous one- and two-item objectives, runs three seeded global searches, and checks independent midpoint quadrature. | VERIFIED · MEDIUM; official Torch training is replaced by a clean-room deterministic optimizer |
| C6 / OT characterization | Optimal-transport dual potentials are generalized convex and the twist inverse recovers the map. | c6_ot.py checks symbolic dual implications with SMT/Fraction-style arithmetic and tests nonquadratic coordinate twist maps in dimensions 2, 4, and 8. | VERIFIED · HIGH |

Primary evidence is organized under
[evidence/claims](evidence/claims). The illustrated report is
[reports/reproduction/report.md](reports/reproduction/report.md), and the
visibility/release audit is
[reports/reproduction/release_report.md](reports/reproduction/release_report.md).

## How each claim is produced

The fixed entrypoint is:

~~~bash
uv run --frozen python repro/src/verify.py
~~~

The verifier first reconstructs the historical finite-grid artifact and
requires that baseline to remain rejected. It then runs one scoped verifier per
claim:

~~~text
verify.py
 ├─ c1_proof.py      compact-net proof certificate
 ├─ c2_audit.py      topology audit and four research routes
 ├─ c3_search.py     exact lean-set counterexample
 ├─ c4_table.py      exact reported-number comparison
 ├─ c5_mechanism.py  continuous one/two-item revenue
 └─ c6_ot.py         OT dual certificate and twist-map inversion
~~~

Each verifier records assumptions, source anchors, raw output, an independent
or arithmetic checker, a negative control, and limitations.

Important evidence details:

- C1 uses a universal compact-net certificate rather than a finite grid.
- C2’s boundary sequence has function error 1/n but gradient error 1 at x=1;
  this falsifies the supporting proposition as written, not the existential
  density theorem itself.
- C3’s exact midpoint counterexample uses
  Phi=[[0,−2,0],[0,0,1]], f=[0,−2,0], and g=[0,0,1].
- C4 differs only at the literal “exactly” predicate; a tolerance of 0.001
  would erase the mismatch.
- C5 recovers p=0.5 and revenue 0.25 for one item, and approximately
  p1=0.6666667, p2=0.8619288, revenue=0.5492010 for two items.
- C6 recovers nonquadratic twist maps with maximum inverse error at most
  3.11e−15; the non-twist control correctly loses uniqueness.

The environment is Python 3.12 with committed pyproject.toml and uv.lock.
Formal runs used CPU-only execution with one requested numerical thread.

## Branch map

The original experiment branches have been renamed so their purpose is visible:

| Clean branch | Former branch | Purpose |
| --- | --- | --- |
| main | main | Publication surface and current documentation |
| historical/judged-baseline | orx/judged-5-12-historical-baseline | Historical finite-grid artifact and rejected baseline |
| audit/c1-compact-cover | orx/c1-compact-cover-proof-certificate | Universal compact-net proof certificate |
| audit/c2-gradient-topology | orx/c2-topology-audit-and-falsification-routes | Four-route gradient-topology audit |
| audit/c3-lean-set | orx/c3-lean-set-exact-counterexample-search | Exact lean-set counterexample |
| audit/c4-table-exact-match | orx/c4-table-i-exact-match-source-audit | Exact Table I audit |
| audit/c5-auction-recovery | orx/c5-continuous-one-two-item-mechanism-recovery | Continuous auction mechanism recovery |
| audit/c6-ot-duality | orx/c6-symbolic-ot-duality-and-nonquadratic-twist-ma | Symbolic OT duality and nonquadratic maps |
| release/evaluator-candidate | orx/evaluator-visible-release-candidate-and-cumulati | Evaluator-visible cumulative release |

The former refs are retained only as provenance in this table and are removed
from the published active branch set after the clean refs are verified.

## Repository contents

- [repro/src/verify.py](repro/src/verify.py): fixed cumulative entrypoint.
- [repro/src/c1_proof.py](repro/src/c1_proof.py): C1 certificate.
- [repro/src/c2_audit.py](repro/src/c2_audit.py): C2 topology and route audit.
- [repro/src/c3_search.py](repro/src/c3_search.py): C3 exact search/checker.
- [repro/src/c4_table.py](repro/src/c4_table.py): C4 exact arithmetic audit.
- [repro/src/c5_mechanism.py](repro/src/c5_mechanism.py): C5 continuous auction
  verifier.
- [repro/src/c6_ot.py](repro/src/c6_ot.py): C6 OT certificate and map recovery.
- [evidence/claims](evidence/claims): claim contracts, methods, raw outputs,
  source audits, and controls.
- [reports/reproduction/report.md](reports/reproduction/report.md): detailed
  evidence report.
- [reports/reproduction/release_report.md](reports/reproduction/release_report.md):
  release and evaluator-visibility record.
- [notebooks/reproduction.py](notebooks/reproduction.py): reader-facing
  tutorial notebook.
- [branch-audit.md](branch-audit.md): normalized branch and claim mapping.

## Citation

~~~bibtex
@article{nehzati2025universal,
  title         = {Universal Representation of Generalized Convex Functions and their Gradients},
  author        = {Moeen Nehzati},
  journal       = {arXiv preprint arXiv:2509.04477},
  year          = {2025},
  doi           = {10.48550/arXiv.2509.04477}
}
~~~

## Thank you

Thank you to Moeen Nehzati for making this work available. The paper’s
combination of generalized convex analysis, optimal transport, and auction
applications made it possible to structure an unusually broad reproduction
around claim-specific proof certificates, exact counterexamples, and continuous
objectives. This repository is an independent reproduction audit, not an
official author implementation.

## Scope and limitations

C1 and C6 use reconstructed symbolic derivations to address universal
quantifiers; finite examples are independent checks, not substitutes for those
proofs. C2 remains unresolved because its function space and gradient topology
need clarification. C4 addresses only the literal exact-match wording. C5 is
medium confidence because the official Torch training loop was replaced by a
clean-room deterministic optimizer. The historical rejected baseline remains
available as provenance, but current statuses are defined by the claim ledger
above.

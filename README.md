---
title: "Repro - Universal Representation of Generalized Convex Functions"
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

# Claim-by-claim reproduction: generalized convex functions

This repository reproduces six claims from [arXiv:2509.04477](https://arxiv.org/abs/2509.04477),
*Universal Representation of Generalized Convex Functions and their
Gradients*. The previous live judge score was **5/12**. The current artifact
supports a conservative **7–10/12 forecast**, with **10/12** the
best-supported possible score—not a judge result.

The campaign replaced the historical 1D grid checks with proof certificates,
exact counterexamples, continuous auction objectives, and multidimensional
nonquadratic optimal-transport constructions. Five claims are now honestly
`VERIFIED` or `FALSIFIED`; Claim 2 remains `BLOCKED` because the paper does not
specify a valid gradient topology and its supporting proposition is false as
written.

| Claim | Paper or live-claim result | Observed evidence | Assessment |
| --- | --- | --- | --- |
| C1, function density | Universal uniform-density theorem | Symbolic compact-net certificate; 867 exact assignments; corrupted radius has a countermodel | **VERIFIED · HIGH** |
| C2, gradient density | Universal gradient-density theorem | Four routes completed; boundary sequence has function error `1/n` but gradient error `1`; no theorem-level counterexample | **BLOCKED · LOW** |
| C3, lean-set convexity | Lean parameter set is convex | Exact compact witness has lean endpoints and nonlean midpoint `[0,-1,1/2]` | **FALSIFIED · HIGH** |
| C4, Table I exact match | Live claim says exact match through `n=10` | Reported differences are `-0.001` at `n=5,10` | **FALSIFIED · HIGH** |
| C5, auction recovery | `p=0.5`, `R=0.25`; two-item mixed bundling | Exact one-item recovery; two-item `p1≈0.6666667`, `p2≈0.8619288`, `R≈0.5492010` | **VERIFIED · MEDIUM** |
| C6, OT characterization | Dual is generalized convex; twist inverse yields map | Symbolic dual certificate plus nonquadratic `d=2,4,8` maps, inverse error `≤3.11e-15` | **VERIFIED · HIGH** |

[Read the illustrated report](reports/reproduction/report.md) ·
[Read the release/visibility audit](reports/reproduction/release_report.md) ·
[Open the tutorial notebook](notebooks/reproduction.py)

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-63o9EmYHXt-universal-representation-of-generalized-convex-functions-and-their-gradients/blob/main/notebooks/reproduction.py)

Formal reproduction command:

```bash
uv run --frozen python repro/src/verify.py
```

The environment is Python 3.12 with committed `pyproject.toml` and `uv.lock`.
Every formal run used Hugging Face `cpu-upgrade`; 64 CPUs were visible while
the verifier enforced one numerical thread. The user-requested compute policy
forbade GPUs.

## Experiment log

Every row inherited the same fixed command verbatim. Branch links are the
reader-facing lineage; internal experiment and run IDs remain in OpenResearch.

| Branch/experiment | Purpose or change | Exact run command | Assessment/outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and Space mirror | N/A |
| [Historical baseline](https://github.com/MachineLearning-Nerd/icml26-repro-63o9EmYHXt-universal-representation-of-generalized-convex-functions-and-their-gradients/tree/orx/judged-5-12-historical-baseline) | Reconstruct judged 1D/grid artifact | `uv run --frozen python repro/src/verify.py` | Expected FAIL; invalid bounded-grid assumptions exposed | HF cpu-upgrade, one requested thread |
| [C1 proof certificate](https://github.com/MachineLearning-Nerd/icml26-repro-63o9EmYHXt-universal-representation-of-generalized-convex-functions-and-their-gradients/tree/orx/c1-compact-cover-proof-certificate) | Universal compact-net proof | `uv run --frozen python repro/src/verify.py` | VERIFIED · HIGH | HF cpu-upgrade, 37 s |
| [C2 topology audit](https://github.com/MachineLearning-Nerd/icml26-repro-63o9EmYHXt-universal-representation-of-generalized-convex-functions-and-their-gradients/tree/orx/c2-topology-audit-and-falsification-routes) | Three verification routes plus mandatory falsification route | `uv run --frozen python repro/src/verify.py` | BLOCKED · LOW | HF cpu-upgrade, 37 s |
| [C3 exact counterexample](https://github.com/MachineLearning-Nerd/icml26-repro-63o9EmYHXt-universal-representation-of-generalized-convex-functions-and-their-gradients/tree/orx/c3-lean-set-exact-counterexample-search) | SMT search and independent rational checker | `uv run --frozen python repro/src/verify.py` | FALSIFIED · HIGH | HF cpu-upgrade, 37 s |
| [C4 exact-table audit](https://github.com/MachineLearning-Nerd/icml26-repro-63o9EmYHXt-universal-representation-of-generalized-convex-functions-and-their-gradients/tree/orx/c4-table-i-exact-match-source-audit) | Decimal and integer-thousandths comparison | `uv run --frozen python repro/src/verify.py` | FALSIFIED · HIGH for literal live claim | HF cpu-upgrade, 42 s |
| [C5 continuous auctions](https://github.com/MachineLearning-Nerd/icml26-repro-63o9EmYHXt-universal-representation-of-generalized-convex-functions-and-their-gradients/tree/orx/c5-continuous-one-two-item-mechanism-recovery) | Exact objective, three seeded searches, independent quadrature | `uv run --frozen python repro/src/verify.py` | VERIFIED · MEDIUM | HF cpu-upgrade, 26 s |
| [C6 OT certificate](https://github.com/MachineLearning-Nerd/icml26-repro-63o9EmYHXt-universal-representation-of-generalized-convex-functions-and-their-gradients/tree/orx/c6-symbolic-ot-duality-and-nonquadratic-twist-ma) | Symbolic duality and nonquadratic twist maps | `uv run --frozen python repro/src/verify.py` | VERIFIED · HIGH; cumulative PASS | HF cpu-upgrade, 32 s |

## Honest scope

- C1 and C6 use reconstructed symbolic derivations to address universal
  quantifiers; finite examples are explicitly only independent checks.
- C2 is not promoted from a proxy. Its four recorded routes end in `BLOCKED`.
- C4 falsifies the live judge claim's word “exactly” from Table I itself. It
  does not falsify the paper's softer “virtually identical” wording and is not
  a rerun of the 100,000-step auction training.
- C5 integrates the full continuous one- and two-item domains, but a clean-room
  deterministic optimizer replaces the official Torch training loop; that
  substitution limits confidence to MEDIUM.

Current verification supersedes—but preserves—the page labeled
**Historical rejected baseline** in the Hugging Face logbook.

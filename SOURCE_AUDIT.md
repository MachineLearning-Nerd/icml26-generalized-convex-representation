# Source audit

## Paper

- Title: *Universal Representation of Generalized Convex Functions and their
  Gradients*
- Author: Moeen Nehzati
- Source: [arXiv:2509.04477](https://arxiv.org/abs/2509.04477)
- Audited version: arXiv v3, revised 12 May 2026

The source anchors cover generalized-convex function density, gradient density,
lean-set convexity, Table I, auction recovery, and optimal-transport duality.
This repository is an independent reproduction audit, not an author-maintained
implementation.

## Paper anchors used

- Function-density theorem and compact-net construction
- Gradient-density theorem and its supporting topology proposition
- Lean finite parameter-set convexity statement
- Table I exact-match statement
- One- and two-item auction application
- Optimal-transport dual potentials and twist inverse

The audit keeps universal proof obligations separate from finite counterexamples
and clean-room numerical recovery. C2 is blocked because its topology boundary
needs clarification.

## Implementation boundary

The repository contains proof certificates, exact rational/SMT searches,
continuous auction objectives, symbolic OT checks, and seeded numerical routes.
The C5 official Torch training loop and the historical finite-grid baseline are
not treated as equivalent to the current claim-level evidence.

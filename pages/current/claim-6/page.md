# C6 — Kantorovich potentials and twist-map recovery

## Exact implication chain and assumptions

Section IV.A states that an optimal Kantorovich dual pair may be normalized to
`(phi,phi^X)` with `phi` generalized convex. At a differentiable
complementary-support point,
`grad(phi)(x)=grad_x(Phi)(x,y)`. If
`y→grad_x(Phi)(x,y)` is a diffeomorphism onto the observed gradient, its
inverse uniquely gives the Monge map.

The contract explicitly assumes an optimal finite-valued dual pair with
defined expectations, differentiability at the evaluated point, and the
stated diffeomorphism/image condition.

Source anchors `#S4.SS1.p11`, `#S4.SS1.p17`, `#S4.SS1.p19`,
`#S4.SS1.p21`; source SHA-256
`238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a`.

## Universal certificate and independent checker

The order certificate shows: feasibility gives `h^X≤k`; replacing `k` by
`h^X` cannot raise the objective; biconjugating lowers `h` while preserving
feasibility; order reversal and feasibility give the triple-transform
identity. Complementary equality makes `phi-Phi(.,y)` attain a differentiable
minimum, yielding the gradient identity.

```text
Paper-specific SMT schemas: 5/5 unsat under negation
Independent exact Fraction cases: 112/112
Infimum-for-supremum corruption: infeasible in 112/112
```

## Multidimensional nonquadratic map checks

Use `Phi(x,y)=sum_i x_i(y_i+a_i y_i^3)` with
`T(x)=diag(alpha)x` and the target measure defined as `T#mu`.
Exact conjugates give dual feasibility and pointwise equality on `(x,T(x))`;
weak duality certifies optimality.

| Dimension | Exact primal-dual value | Maximum inverse error | Maximum complementary slack |
| ---: | ---: | ---: | ---: |
| 2 | `10757/15360` | `3.11e-15` | `4.44e-16` |
| 4 | `52233/40960` | `2.78e-15` | `4.44e-16` |
| 8 | `477943/196608` | `3.11e-15` | `8.88e-16` |

Non-twist control: `Phi_bad=x y²` has `grad_x=y²`; destinations `-1/2` and
`1/2` share gradient `1/4`, so a principal inverse makes a one-unit error for
the negative destination. Uniqueness fails for exactly the intended reason.

- [Executable proof and map verifier](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/repro/src/c6_ot.py)
- [Raw formal output](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c6/raw_run_f5de8621.json)
- [Claim contract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c6/claim_contract.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c6/source_audit.md)

Formal command: `uv run --frozen python repro/src/verify.py`.
Git SHA `e543df69ac0bb2b63011e572a8e6368148708e52`; Sobol seed
`20250906`; HF cpu-upgrade; estimated one numerical core with uncertain
cumulative runtime; 64 visible CPUs; one requested thread; job 32 s; verifier
0.669102 s.

## Reviewer verdict

**VERIFIED · HIGH · expected 2/2.** The universal portion rests on the
machine-checkable symbolic derivation; the d=2,4,8 cases are independent
nonquadratic corroboration, not a finite proxy for universality. Existence and
regularity remain explicit assumptions.

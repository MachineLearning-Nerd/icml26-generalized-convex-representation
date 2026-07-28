# Claim 6 source audit

Source: ar5iv rendering of arXiv:2509.04477, retrieved 2026-07-28 with an
explicit browser User-Agent. SHA-256:
`238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a`.

## Exact source chain

- Section IV.A, `#S4.SS1.p11`: from any optimal feasible dual pair, replace
  the second potential by the first potential's generalized transform, then
  biconjugate the first potential. The resulting first potential is
  generalized convex and the second is its transform.
- `#S4.SS1.p17`: on complementary support, differentiable equality implies
  `grad(phi)(x) = grad_x(Phi)(x,y)`.
- `#S4.SS1.p19`: when `y -> grad_x(Phi)(x,y)` is a diffeomorphism, invert it
  to recover the transportation map.
- `#S4.SS1.p21`: the section summarizes these as characterizations of the
  Kantorovich and Monge solutions.

## Assumption audit

The representation step presupposes existence of an optimal dual pair and
finite, integrable potentials. The gradient step additionally requires
differentiability at the complementary point. The Monge-map step additionally
requires the stated twist/diffeomorphism condition and that the observed
gradient lies in its image. These conditions are explicit in the claim
contract and are not inferred from a finite numerical example.

## Quantifiers

The normalization argument applies to every optimal feasible pair for which
the stated transform and expectations are defined. The map identity applies
at each differentiability point on complementary support. Unique recovery is
conditional on the diffeomorphism condition.

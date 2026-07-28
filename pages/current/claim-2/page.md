# C2 — gradient density

## Exact claim and source problem

Theorem 2 says that under semiconvexity of `Phi`, gradients of finitely
`Y`-convex functions are dense in gradients of all `Y`-convex functions.
The paper says convergence is uniform “where gradients exist,” but does not
define the gradient function space or topology. Its Proposition 3 claims that
uniform convergence of equi-semiconvex functions implies uniform gradient
convergence wherever both gradients exist.

Source anchors `#Thmproposition3` and `#Thmtheorem2`; source SHA-256
`238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a`.

## Exactly four completed routes

1. **Primary-source topology audit.** The cited result requires an open convex
   domain, differentiable convex functions, and uniform convergence only on
   compact subsets of the interior. These conditions are absent from the
   paper statement.
2. **Exact proposition counterexample.** On `[0,1]`,
   `f_n=max(0,x-(1-1/n))` and `f=0` are convex with shared semiconvex constant
   zero. Function error is `1/n`, but the gradient error at `x=1` is exactly
   one for every `n=2,4,...,128`.
3. **Corrected smooth/interior route.** Max-tangent approximants to
   `f=x²/2` have exact gradient bounds `1/4,1/8,...,1/128` away from ties.
   This verifies a corrected special case, not the stated theorem.
4. **Mandatory falsification route.** The boundary sequence cannot falsify
   existential density because `f=0` itself has an exact finite
   representation. The invalid inference from one bad sequence was explicitly
   rejected.

Control `h_n=x²/(2n)` has gradient error `1/n` and converges as expected. A
fixed-three-support corruption in route 3 has nonvanishing error `1/4`.

- [Executable audit](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/repro/src/c2_audit.py)
- [Claim contract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c2/claim_contract.json)
- [Raw route summary](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c2/raw_run_0f46ec76.json)
- [All four route interpretations and controls](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c2/routes.json)
- [Exact Proposition 3 counterexample rows](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c2/proposition_counterexample.csv)
- [Corrected interior-route rows](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c2/corrected_interior_route.csv)
- [Source audit](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c2/source_audit.md)

Formal command: `uv run --frozen python repro/src/verify.py`.
Git SHA `b566feca9371ff39ff85999f822e61afc9a3df0b`; deterministic; HF
cpu-upgrade; estimated one core; 64 visible CPUs; one requested thread; job
37 s; verifier 0.182674 s.

## Reviewer verdict

**BLOCKED · LOW · expected 0/2 under the strict exact-claim rubric.** The four
required routes are complete. Unblocker: an author-specified topology plus a
corrected proof, or a counterexample that satisfies that precise topology and
contradicts the existential statement.

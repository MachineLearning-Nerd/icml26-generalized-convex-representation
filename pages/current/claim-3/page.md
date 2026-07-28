# C3 — convexity of the lean parameter set

## Exact claim and assumptions

For a fixed finite support, Theorem 4 states that the lean parameter subset is
convex. The v1 global assumptions are compact Euclidean `X,Y` and locally
Lipschitz finite `Phi`; a parameter is lean when every support is active
somewhere.

Source anchors `#S5.SS3`, `#Thmtheorem3`, `#Thmtheorem4`; source SHA-256
`238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a`.

## Exact counterexample

```text
X = {0,1}, Y_tilde = {0,1,2}
Phi = [[0,-2,0],
       [0, 0,1]]
first  = [0,-2,0]       lean
second = [0, 0,1]       lean
midpoint = [0,-1,1/2]   nonlean
```

At the midpoint, support 2 is strictly dominated by support 0 on the first
row and support 1 on the second. Finite sets are compact, all suprema are
attained, and a finite Lipschitz upper bound is 3.

```text
SMT witness: sat
Independent Fraction checker: endpoints lean, midpoint nonlean
Lost support: 2
Identical-endpoint negative control: unsat
Process verdict: FALSIFIED
```

- [Executable search and checker](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/repro/src/c3_search.py)
- [Claim contract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c3/claim_contract.json)
- [Raw HF output extract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c3/raw_run_b7e56a29.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c3/source_audit.md)

Formal command: `uv run --frozen python repro/src/verify.py`.
Git SHA `0487ce3e37a507225ff245395797191463c14d60`; deterministic SMT and
rational arithmetic; HF cpu-upgrade; estimated one core; 64 visible CPUs; one
requested thread; job 37 s; verifier 0.228176 s.

## Reviewer verdict

**FALSIFIED · HIGH · expected 2/2.** The witness satisfies every stated v1
assumption and contradicts the universal convexity statement. It does not
claim failure under extra unstated restrictions such as continuum convex
domains with bilinear surplus.

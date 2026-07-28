# C1 — universal function density

## Exact claim and assumptions

For every `epsilon>0` and every `f∈C^Y(X)`, there is a finite
`Y_tilde⊂Y` and `g∈C^{Y_tilde}(X)` with
`||f-g||_infinity<epsilon`. Assumptions audited from Theorem 1 and Section V:
compact nonempty Euclidean `X,Y`, a shared finite Lipschitz constant for
`Phi` on `X×Y`, `f=f^{YX}`, and the uniform norm.

Source: ar5iv arXiv:2509.04477, anchors `#S5.p3`, `#S5.SS1`,
`#Thmtheorem1`; retrieved 2026-07-28; SHA-256
`238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a`.

## Method and raw result

The verifier reconstructs the compact finite-net proof rather than sampling
functions. A radius `epsilon/(4 lambda)` makes each selected branch differ by
at most `epsilon/2`; support inclusion gives the other one-sided inequality.
The zero-Lipschitz case is separate.

```text
Z3 negated local bound: unsat
Independent exact assignments: 867
Largest normalized positive gap: 1/2
Corrupted radius 3 epsilon/(4 lambda): sat
Corrupted normalized gap: 3/2
Process verdict: VERIFIED
```

The **negative control** is the corrupted larger radius. It must produce a
satisfying countermodel with normalized gap `3/2`; a verifier that accepts
that radius would therefore fail the contract.

- [Executable verifier](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/repro/src/c1_proof.py)
- [Claim contract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c1/claim_contract.json)
- [Proof certificate](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c1/proof_certificate.json)
- [Raw HF output extract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c1/raw_run_c8bc7870.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c1/source_audit.md)

Formal command: `uv run --frozen python repro/src/verify.py`.
Git SHA `00f6c4b703bbc9061ea04eaededf53c701ee11a1`; deterministic, no
stochastic seed; HF cpu-upgrade; estimated one core; 64 visible CPUs; one
requested numerical thread; job 37 s; verifier 0.180453 s.

## Reviewer verdict

**VERIFIED · HIGH · expected 2/2.** This is a symbolic reconstruction of the
universal compactness argument, not finite empirical corroboration. The
standard compact finite-subcover theorem is the declared trusted primitive.
The historical grid is preserved only as **Historical rejected baseline**.

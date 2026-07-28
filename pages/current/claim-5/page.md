# C5 — one- and two-item auction recovery

## Exact claim and continuous domain

Figures 2–3 report recovery of the one-item posted price `1/2`, revenue
`1/4`, and the two-item mixed-bundling menu. The clean-room verifier uses the
complete `Uniform([0,1])` and `Uniform([0,1]^2)` domains, not a finite buyer
grid. For two items its four menu branches are no allocation, either singleton
at price `p1`, and the bundle at price `p2`.

The primary theoretical benchmark is:

```text
p1 = 2/3 = 0.6666666666666666
p2 = (4-sqrt(2))/3 = 0.8619288125423017
revenue = 0.5492010046202292
```

Source anchors `#S7.F2`, `#S7.F3`; paper source SHA-256
`238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a`.
Benchmark reference: Giannakopoulos and Koutsoupias, arXiv:1404.2329.

## Observed evidence

One item recovers `p=0.5`, `R=0.25` exactly. Three independent seeded global
searches recover:

| Seed | `p1` | `p2` | Revenue |
| ---: | ---: | ---: | ---: |
| 20250905 | 0.6666668170 | 0.8619287043 | 0.5492010046202077 |
| 20250906 | 0.6666667468 | 0.8619286748 | 0.5492010046202120 |
| 20250907 | 0.6666663487 | 0.8619289323 | 0.5492010046201599 |

Price spread is at most `4.69e-7`; revenue spread is `5.22e-14`.
Independent midpoint integration gives `0.54943855`, `0.54929493`,
`0.54936540` at side lengths 200, 400, 800.

Controls:

```text
separate selling revenue = 0.5000000000
pure bundle revenue      = 0.5443310540
mixed bundling revenue   = 0.5492010046
```

Both restricted controls underperform by more than the predeclared `0.003`.

- [Executable continuous verifier](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/repro/src/c5_mechanism.py)
- [Raw optimizer/checker output](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c5/raw_run_c6b3d274.json)
- [Claim contract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c5/claim_contract.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c5/source_audit.md)

Formal command: `uv run --frozen python repro/src/verify.py`.
Git SHA `6fc688ddf199b5491a9bdac2c1ce63eb2f4604a7`; seeds above; HF
cpu-upgrade; estimated one numerical core with uncertain runtime; 64 visible
CPUs; one requested thread; job 26 s; verifier 0.468200 s.

## Reviewer verdict

**VERIFIED · MEDIUM · expected 2/2.** The continuous objective, mechanism, and
independent integration are faithful. The clean-room deterministic global
optimizer replaces the official 100,000-step Torch training loop, so the page
does not claim an exact training-code reproduction.

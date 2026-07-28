# C4 — Table I “exact” benchmark match

## Exact claim and scope

The live judged claim says that for `n≤10`, the learned per-item revenue
matches the Straight-Jacket benchmark **exactly**. Table I itself reports:

| Goods | Learned | Straight-Jacket | Signed difference | Exact at reported precision? |
| ---: | ---: | ---: | ---: | --- |
| 1 | 0.250 | 0.250 | 0.000 | yes |
| 2 | 0.274 | 0.274 | 0.000 | yes |
| 5 | 0.314 | 0.315 | -0.001 | **no** |
| 10 | 0.346 | 0.347 | -0.001 | **no** |

Source anchors `#S7.T1` and `#S7.p6`; source SHA-256
`238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a`.
The paper's own prose says “virtually identical,” which is softer than the
live claim audited here.

## Checker and control

Python `Decimal` arithmetic and an independent integer-thousandths checker
both identify mismatches at `n=5,10`. The negative control replaces equality
with `absolute difference ≤0.001`; that corrupted predicate passes every row
and is rejected because it does not test “exactly.”

- [Executable table audit](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/repro/src/c4_table.py)
- [Raw Table I CSV](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c4/table_i.csv)
- [Raw HF output extract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c4/raw_run_3142314a.json)
- [Claim contract](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c4/claim_contract.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/claims/c4/source_audit.md)

Formal command: `uv run --frozen python repro/src/verify.py`.
Git SHA `ac3da7c456ff00420002327bbd9fd3e5e45b349f`; deterministic; HF
cpu-upgrade; estimated one core; 64 visible CPUs; one requested thread; job
42 s; verifier 0.220336 s.

## Reviewer verdict

**FALSIFIED · HIGH · expected 2/2 for the literal live claim.** This is direct
reported-number evidence, not a rerun of the 100,000-step mechanism training.
It does not falsify the paper's “virtually identical” wording. That semantic
scope is the remaining evaluator risk.

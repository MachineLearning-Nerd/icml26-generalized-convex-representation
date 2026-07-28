# Claim-by-claim reproduction — current evidence

**Previous live judged score: 5/12. Conservative forecast: 7–10/12.
Best-supported possible score: 10/12. These are forecasts, not a new judge
result.**

This is the canonical evaluator entrypoint for arXiv:2509.04477. Current
verification is first in navigation and supersedes the old weak verifier. The
old pages remain reachable under the exact label **Historical rejected
baseline** and are unchanged from judged revision
`90cdeabce1e7b901ad6fe1ea8f49cebee8e8417f`.

## Current results

| Claim | Exact status | Confidence | Canonical evidence |
| --- | --- | --- | --- |
| C1 function density | **VERIFIED** | HIGH | [Claim 1](#/current/claim-1) |
| C2 gradient density | **BLOCKED** | LOW | [Claim 2 and all four routes](#/current/claim-2) |
| C3 lean-set convexity | **FALSIFIED** | HIGH | [Claim 3](#/current/claim-3) |
| C4 Table I exact match | **FALSIFIED** | HIGH | [Claim 4](#/current/claim-4) |
| C5 one/two-item recovery | **VERIFIED** | MEDIUM | [Claim 5](#/current/claim-5) |
| C6 OT characterization | **VERIFIED** | HIGH | [Claim 6](#/current/claim-6) |

[Read the current overview](#/current) ·
[Inspect the complete visibility matrix and red-team audit](#/current/visibility) ·
[Download the illustrated report](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/reports/reproduction/report.md)

## Reproduce

```bash
uv run --frozen python repro/src/verify.py
```

The candidate includes the executable `repro/src` tree, Python 3.12
`pyproject.toml`, exact `uv.lock`, claim contracts, raw JSON/CSV, source audits,
independent-checker output, controls, and limitations. Formal jobs used
Hugging Face `cpu-upgrade`; 64 CPUs were visible and the program enforced one
numerical thread. No GPU was used.

Current cumulative verifier commit:
`e543df69ac0bb2b63011e572a8e6368148708e52`.
The final release-candidate regression SHA and published HF revision are
recorded on the [visibility page](#/current/visibility).

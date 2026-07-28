# Historical rejected baseline

This is the canonical page for the frozen starting node.

- Judged Space: `DineshAI/63o9EmYHXt@90cdeabce1e7b901ad6fe1ea8f49cebee8e8417f`
- Live judged score: `5/12`
- Fixed command: `uv run --frozen python repro/src/verify.py`
- Scientific workload estimate: one CPU core, under five minutes
- Submission choice: Hugging Face `cpu-upgrade`, because first-run locked
  environment materialization has uncertain runtime; the verifier itself
  requests one numerical thread and prints the visible CPU allocation.
- Current scientific result: all six claims remain **BLOCKED** at this node.

The command reconstructs the five toy checks and the deferred auction check, prints all raw results as JSON, and exits nonzero if the historical regression no longer behaves as recorded. It does not call a toy result VERIFIED.

## Exact C1 contract

Theorem 1 states that for every `epsilon > 0` and every `f ∈ C^Y(X)`, there exists a finite `Y~ ⊂ Y` and `g ∈ C^{Y~}(X)` such that `||f-g||∞ < epsilon`, under the paper's compactness and kernel regularity assumptions.

The finite 1D check does not discharge those quantifiers. See `../claims/c1/claim_contract.json`, `method.md`, and `EVAL.md`.

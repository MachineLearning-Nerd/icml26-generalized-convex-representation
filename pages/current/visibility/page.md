# Visibility matrix and evaluator-blind audit

This page is part of the release gate. The candidate is traversed from
`pages/index.md` without using OpenResearch logs, unpublished branches, or
repository-only knowledge.

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | `#/current/claim-1` | yes | yes | yes | Z3 + 867 exact | radius countermodel | yes | VERIFIED · HIGH |
| C2 | `#/current/claim-2` | yes | yes | yes | four-route audit | convergent smooth sequence + fixed support | yes | BLOCKED · LOW |
| C3 | `#/current/claim-3` | yes | yes | yes | SMT + Fraction | identical endpoints UNSAT | yes | FALSIFIED · HIGH |
| C4 | `#/current/claim-4` | yes | yes | yes | Decimal + integer | tolerance false positive | yes | FALSIFIED · HIGH |
| C5 | `#/current/claim-5` | yes | yes | yes | analytic + quadrature | pure bundle/separate | yes | VERIFIED · MEDIUM |
| C6 | `#/current/claim-6` | yes | yes | yes | SMT + Fraction + roots | infimum + non-twist | yes | VERIFIED · HIGH |

Every page also exposes assumptions, source hash/anchors, fixed command,
pinned environment links, Git SHA, deterministic seeds, CPU allocation,
runtime, limitations, and a verifier that contributes to a nonzero cumulative
exit on failure.

## Historical safety

Judged revision:
`90cdeabce1e7b901ad6fe1ea8f49cebee8e8417f`.
Its file manifest is downloadable
[here](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/evidence/provenance/judged_space_90cdeab_manifest.sha256).
The old `pages/verify/page.md` and `pages/overview/page.md` are byte-for-byte
unchanged and remain reachable under **Historical rejected baseline**. The
current verifier is first in navigation and explicitly supersedes them.

## Evaluator-blind red team

The final pre-publication audit record is mirrored in
[`reports/reproduction/release_report.md`](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/reports/reproduction/release_report.md)
and the complete
[`release/red_team.md`](https://huggingface.co/spaces/DineshAI/63o9EmYHXt/resolve/main/release/red_team.md).
Round 1 failed because C1's corrupted-radius countermodel was not explicitly
labeled as a control. The page was fixed. The audit records every file opened,
that missing conclusion, the fix, and the required fresh Round 2 traversal.
The published HF revision and post-publication hash verification are appended
to the public release record only after every gate passes.

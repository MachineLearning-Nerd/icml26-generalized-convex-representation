# Evaluator-blind pre-publication review

Scope: review only a fresh candidate Space checkout, starting from
`README.md`, `logbook.json`, and `pages/index.md`. Do not use OpenResearch
logs, dashboard files, unpublished branches, or prior repository knowledge.

## Round 1 — failed discoverability gate

Candidate source commit:
`afdbd8141d7c108d1b002e007a11d3afe60332df`.
The initial invocation used the fresh candidate script but inherited the
repository cwd, so it was not accepted as a valid blind traversal. It still
identified a real page defect: C1 exposed the corrupted radius and satisfying
countermodel but did not explicitly call them a control. The page now labels
the countermodel **negative control** and states its intended failure.

Files opened before that stopped conclusion:

```text
README.md
logbook.json
pages/index.md
pages/current/page.md
pages/current/claim-1/page.md
pages/current/claim-2/page.md
pages/current/claim-3/page.md
pages/current/claim-4/page.md
pages/current/claim-5/page.md
pages/current/claim-6/page.md
pages/current/visibility/page.md
pages/verify/page.md
pages/overview/page.md
```

## Round 1b — valid fresh-directory preservation failure

Candidate source commit:
`e936ee0c008772d429d6377533d16b496b3da9ea`.
Fresh directory: `/tmp/orx-space-candidate-round2.WTuOK3`.
The audit was rerun from inside that directory. It opened the canonical pages,
claim artifacts, verifier sources, and report figures, then stopped at the
historical hash check.

Conclusion that could not be verified: byte identity of
`pages/overview/page.md`. Direct hashing showed that the page *was*
byte-identical, but the original protected manifest contained a 63-character
hash: its final hexadecimal nibble `f` had been omitted.

Fix: preserve the original manifest, add
`judged_space_90cdeab_manifest_corrected.sha256` with the complete judged-tree
hashes, and make the audit use that corrected derivative. No historical file
was changed.

## Round 2 — required repeat

Candidate source commit:
`2f18caadfd991da3369bba67c2391274cf319710`.
Fresh directory: `/tmp/orx-space-candidate-round2-valid.7Mgia0`.
The directory began as a fresh clone checked out at the exact judged Space
revision, then received only the declared text allowlist. The audit ran from
inside that candidate directory.

Files opened:

```text
README.md
evidence/claims/c1/EVAL.md
evidence/claims/c1/claim_contract.json
evidence/claims/c1/method.md
evidence/claims/c1/raw_run_c8bc7870.json
evidence/claims/c1/source_audit.md
evidence/claims/c2/EVAL.md
evidence/claims/c2/claim_contract.json
evidence/claims/c2/method.md
evidence/claims/c2/raw_run_0f46ec76.json
evidence/claims/c2/source_audit.md
evidence/claims/c3/EVAL.md
evidence/claims/c3/claim_contract.json
evidence/claims/c3/method.md
evidence/claims/c3/raw_run_b7e56a29.json
evidence/claims/c3/source_audit.md
evidence/claims/c4/EVAL.md
evidence/claims/c4/claim_contract.json
evidence/claims/c4/method.md
evidence/claims/c4/raw_run_3142314a.json
evidence/claims/c4/source_audit.md
evidence/claims/c5/EVAL.md
evidence/claims/c5/claim_contract.json
evidence/claims/c5/method.md
evidence/claims/c5/raw_run_c6b3d274.json
evidence/claims/c5/source_audit.md
evidence/claims/c6/EVAL.md
evidence/claims/c6/claim_contract.json
evidence/claims/c6/method.md
evidence/claims/c6/raw_run_f5de8621.json
evidence/claims/c6/source_audit.md
logbook.json
pages/current/claim-1/page.md
pages/current/claim-2/page.md
pages/current/claim-3/page.md
pages/current/claim-4/page.md
pages/current/claim-5/page.md
pages/current/claim-6/page.md
pages/current/page.md
pages/current/visibility/page.md
pages/index.md
pages/overview/page.md
pages/verify/page.md
reports/reproduction/images/c2-topology.svg
reports/reproduction/images/c4-table.svg
reports/reproduction/images/c5-auction.svg
reports/reproduction/images/c6-twist.svg
reports/reproduction/images/headline-status.svg
reports/reproduction/release_report.md
reports/reproduction/report.md
repro/src/c1_proof.py
repro/src/c2_audit.py
repro/src/c3_search.py
repro/src/c4_table.py
repro/src/c5_mechanism.py
repro/src/c6_ot.py
repro/src/core.py
repro/src/verify.py
```

Result:

```json
{
  "allowlisted_text_files": 73,
  "audit": "PASS",
  "claims_complete": 6,
  "fixed_command": "uv run --frozen python repro/src/verify.py",
  "historical_files_present": 15,
  "historical_pages_byte_identical": true,
  "logbook_pages_opened": 58,
  "report_figures": 5,
  "secrets_detected": false,
  "space_id": "DineshAI/63o9EmYHXt"
}
```

No conclusion remained inaccessible. All visibility-matrix cells were
complete.

## Final repeat after recording Round 2

Candidate source commit:
`9fa0d00daf012b7bc80d07cb322ec7a464d4ccca`.
Fresh directory: `/tmp/orx-space-candidate-final-pre-run.X6ZIKV`.
This was another fresh clone at the exact judged Space revision with only the
candidate allowlist overlaid. The audit again returned `PASS` with the same 58
opened files, six complete claims, 73 text files, 15 historical files, exact
historical-page byte identity, five figures, and no detected secret pattern.
No evidence or navigation fix was needed after the repeat.

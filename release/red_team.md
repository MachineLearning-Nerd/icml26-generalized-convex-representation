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

Publication remains blocked until the corrected candidate is committed,
overlaid onto another fresh exact judged Space checkout, and the complete
traversal passes with no missing conclusion or visibility cell. The immutable
Round 2 opened-file list and result are appended here before formal regression.

- Previous live judged score: `5/12`
- Conservative projected score range after the proposed change: `7–10/12`
- Best-supported possible new score: `10/12` (**forecast, not a judge result**)

# Release and visibility report

The current total score remains **5/12** until the live evaluator judges a new
Hugging Face revision. The proposed artifact resolves five claims with direct
`VERIFIED` or `FALSIFIED` evidence and leaves one claim honestly `BLOCKED`.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| C1 | 1 | 2 | HIGH | VERIFIED | Universal compact-net proof certificate, Z3, and 867 exact assignments; standard finite-subcover theorem is trusted |
| C2 | 1 | 0 | LOW | BLOCKED | Four required routes complete; exact topology is underspecified and no valid theorem-level counterexample was found |
| C3 | 1 | 2 | HIGH | FALSIFIED | Exact compact assumption-satisfying counterexample; risk is an evaluator imposing unstated continuum restrictions |
| C4 | 0 | 2 | HIGH | FALSIFIED | Table I differs by 0.001 at n=5,10; applies only to the live claim's literal “exactly” wording |
| C5 | 1 | 2 | MEDIUM | VERIFIED | Full continuous one/two-item objective and independent quadrature; official Torch loop was replaced |
| C6 | 1 | 2 | HIGH | VERIFIED | Universal dual certificate plus nonquadratic d=2,4,8 maps; existence and differentiability stay explicit |

The conservative projected total is **7–10/12**. The best-supported possible
total is **10/12** under the strict rule that `BLOCKED` earns zero. Forecast
points are not earned points.

## What changed

- C1: toy grid → universal proof certificate.
- C2: toy gradient curve → exact four-route audit ending `BLOCKED`.
- C3: random 1D combinations → exact theorem counterexample.
- C4: deferred auction LP → direct falsification of the live exact-match
  wording from the reported Table I values.
- C5: one-item closed form only → continuous one- and two-item recovery.
- C6: six 1D quadratic cases → universal dual certificate and
  multidimensional nonquadratic twist maps.

C2 remains `BLOCKED` because neither the paper nor its citation supplies a
valid topology matching the stated compact-domain conclusion. It would be
unblocked by an author-specified topology plus corrected proof, or a valid
assumption-satisfying counterexample to that exact statement.

## Experiment tree and winning lineage

The stacked lineage is:

```text
historical baseline
  └─ C1 compact-cover proof
      └─ C2 topology/falsification routes
          └─ C3 exact counterexample
              └─ C4 exact Table I audit
                  └─ C5 continuous mechanisms
                      └─ C6 symbolic OT and twist maps
                          └─ evaluator-visible release candidate
```

The accepted scientific branch is
`orx/c6-symbolic-ot-duality-and-nonquadratic-twist-ma` at
`e543df69ac0bb2b63011e572a8e6368148708e52`. The presentation/release child
will record its final SHA after the cumulative regression.

## Compute and runtime

All formal jobs used HF `cpu-upgrade`, the pinned image
`ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim`, and the fixed command:

```bash
uv run --frozen python repro/src/verify.py
```

Each program requested one numerical thread. HF exposed 64 CPUs. Accepted job
durations were C1 37 s, C2 37 s, C3 37 s, C4 42 s, C5 26 s, and C6 32 s:
**211 seconds total accepted HF wall time**. Baseline used one 37-second
scientific run plus one environment-only non-answer. Local work was limited to
one-core syntax, JSON, notebook, and isolated verifier checks under five
minutes. No GPU was used. HF cost is provider/account dependent and was not
reported by the backend, so no monetary cost is invented.

## Command ledger

Startup and provenance:

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 5d3c2823-b296-4b51-a21f-096aef3ca896
orx paper 2509.04477
git branch -a
git status --short
git rev-parse HEAD
git fetch origin
git ls-remote origin
```

Formal experiment launch template used for each accepted node:

```text
orx exp status <experiment>
orx exp run <experiment> --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim --timeout 1h
orx exp wait <experiment> --interval 10 --timeout 480
orx runs 5d3c2823-b296-4b51-a21f-096aef3ca896 --experiment <experiment>
orx logs <run> --bytes 200000
orx exp desc <experiment> --set <evidence summary>
```

Release checks:

```text
uv run --frozen python -m json.tool logbook.json
marimo check --strict notebooks/reproduction.py
git diff --check
git status --short
sha256sum <allowlisted text files>
git ls-remote origin refs/heads/main
```

No generated run wrapper, token, credential, or secret value is included.
The exact notebook check used marimo 0.23.15 temporarily inside the same
repository `.venv`; `uv sync --frozen` then restored locked marimo 0.14.17
before the formal regression. No second repository environment was created.

## Historical subset and upload

Protected judged HF revision:
`90cdeabce1e7b901ad6fe1ea8f49cebee8e8417f`.
Its old file set must be a strict subset of the candidate tree. The old
`pages/verify/page.md` and `pages/overview/page.md` remain byte-for-byte
unchanged and are labeled **Historical rejected baseline** in current
navigation. The original pre-candidate manifest accidentally omitted the last
hexadecimal nibble from the overview-page hash; it remains preserved, and a
corrected derivative with the full exact hash is the active subset checker.

The exact text-only upload allowlist and SHA-256 manifest are generated under
`release/` after the final candidate regression. No deletion or binary upload
is authorized.

## Evaluator-blind red team

The first blind traversal starts only from candidate `README.md`,
`logbook.json`, and `pages/index.md`, then follows displayed links. It records
every opened file and treats repository-only or OpenResearch-only facts as
missing. Any missing cell triggers a navigation/content fix followed by a
second complete traversal. The final file-open record and conclusions are
stored in `release/red_team.md` and mirrored on the Space visibility page.

## Exact publication action

After all release gates pass, upload only the SHA-manifested text allowlist to
the existing Space `DineshAI/63o9EmYHXt` through the Hugging Face text API,
without creating a second Space or deleting historical files. Then download
the exact published revision, verify every hash, rerun canonical traversal,
record the HF revision, mirror the exact text paths to GitHub `main`, confirm
the remote SHA, and mark the paper awaiting judge. The score remains 5/12
until a live verdict is recorded.

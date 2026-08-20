# Environment and reproduction contract

## Fixed command

~~~bash
uv run --frozen python repro/src/verify.py
~~~

The verifier reconstructs the historical rejected baseline, then runs the six
claim-specific routes and their independent or arithmetic checks.

## Pinned environment

- Python: 3.12
- Dependencies: committed pyproject.toml and uv.lock
- Backend: CPU-only
- Requested numerical threads: 1
- Formal checks: Z3 and exact rational arithmetic
- Numerical checks: deterministic SciPy/NumPy routes
- External data: none

The historical OpenResearch runs used CPU-upgrade resources, but the evidence
files preserve their exact run records and source anchors. No private dataset
is introduced for C4 or any other claim.

## Evidence locations

- Claim implementations: repro/src/
- Claim contracts and raw runs: evidence/claims/
- Provenance: evidence/provenance/
- Detailed report: reports/reproduction/report.md
- Release record: reports/reproduction/release_report.md
- Candidate verifier: release/audit_candidate.py
- Pinned environment: pyproject.toml and uv.lock

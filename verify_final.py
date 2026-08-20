from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
EXPECTED_BRANCHES = {
    "main",
    "historical/judged-baseline",
    "audit/c1-compact-cover",
    "audit/c2-gradient-topology",
    "audit/c3-lean-set",
    "audit/c4-table-exact-match",
    "audit/c5-auction-recovery",
    "audit/c6-ot-duality",
    "release/evaluator-candidate",
}
EXPECTED_COMMITS = 26
EXPECTED_STATUSES = {
    "C1": "VERIFIED_SCOPED",
    "C2": "BLOCKED",
    "C3": "FALSIFIED_SCOPED",
    "C4": "FALSIFIED_SCOPED",
    "C5": "VERIFIED_SCOPED",
    "C6": "VERIFIED_SCOPED",
}
EXPECTED_OVERALL = (
    "PARTIAL_C1_C5_C6_VERIFIED_C2_BLOCKED_C3_C4_FALSIFIED_"
    "HISTORICAL_SCORE_5_OF_12_NO_CURRENT_SCORE"
)


def run(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def read_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"VERIFY_FAILED: {message}")


def published_branches() -> set[str]:
    try:
        output = run("ls-remote", "--heads", "origin")
    except subprocess.CalledProcessError:
        output = run("for-each-ref", "--format=%(refname:short)", "refs/heads/")
        return {line for line in output.splitlines() if line}
    return {
        line.split("refs/heads/", 1)[1]
        for line in output.splitlines()
        if "refs/heads/" in line
    }


def main() -> None:
    claims = read_json("claims.json")
    verdicts = read_json("reproduction_verdicts.json")
    manifest = read_json("EVIDENCE_MANIFEST.json")
    state = read_json("AUTONOMOUS_STATE.json")
    c1 = read_json("evidence/claims/c1/raw_run_c8bc7870.json")
    c2 = read_json("evidence/claims/c2/raw_run_0f46ec76.json")
    c3 = read_json("evidence/claims/c3/raw_run_b7e56a29.json")
    c4 = read_json("evidence/claims/c4/raw_run_3142314a.json")
    c5 = read_json("evidence/claims/c5/raw_run_c6b3d274.json")
    c6 = read_json("evidence/claims/c6/raw_run_f5de8621.json")

    require(published_branches() == EXPECTED_BRANCHES, "published branch set changed")
    require("orx" not in " ".join(published_branches()), "legacy orx branch remains")
    require(run("symbolic-ref", "--short", "HEAD") == "main", "main is not checked out")
    require(int(run("rev-list", "--count", "--all")) == EXPECTED_COMMITS, "reachable commit count changed")

    identities = run("log", "--all", "--format=%an%x09%ae%x09%cn%x09%ce").splitlines()
    expected_identity = "\t".join(
        [CANONICAL_NAME, CANONICAL_EMAIL, CANONICAL_NAME, CANONICAL_EMAIL]
    )
    require(identities and all(line == expected_identity for line in identities), "commit identity is not canonical")

    require(claims["overall_status"] == EXPECTED_OVERALL, "claims overall status mismatch")
    require(verdicts["overall_status"] == EXPECTED_OVERALL, "verdict overall status mismatch")
    require(state["overall_status"] == EXPECTED_OVERALL, "state overall status mismatch")
    require(claims["current_score_claim"] is False, "claims make a current score claim")
    require(verdicts["historical_evaluation"]["current_score_claim"] is False, "verdicts make a current score claim")
    require(state["current_score_claim"] is False, "state makes a current score claim")
    require(verdicts["publication"]["publication_allowed"] is False, "publication boundary changed")

    claim_statuses = {claim["id"]: claim["status"] for claim in claims["claims"]}
    require(claim_statuses == EXPECTED_STATUSES, f"claim statuses are {claim_statuses}")
    require(
        {claim_id: item["status"] for claim_id, item in verdicts["claims"].items()}
        == EXPECTED_STATUSES,
        "machine-readable verdict statuses mismatch",
    )

    require(c1["c1_scientific_verdict"] == "VERIFIED", "C1 result changed")
    require(c1["independent_assignments_checked"] == 867, "C1 audit count changed")
    require(c2["c2_scientific_verdict"] == "BLOCKED", "C2 result changed")
    require(c2["routes_completed"] == 4 and c2["proposition_3_counterexample_verified"] is True, "C2 routes changed")
    require(c3["c3_scientific_verdict"] == "FALSIFIED", "C3 result changed")
    require(c3["midpoint_lost_support"] == 2, "C3 counterexample changed")
    require(c4["c4_scientific_verdict"] == "FALSIFIED", "C4 result changed")
    require(c4["mismatch_dimensions"] == [5, 10], "C4 mismatch changed")
    require(c5["result"]["scientific_verdict"] == "VERIFIED", "C5 result changed")
    require(c5["result"]["verifier_passed"] is True, "C5 verifier result changed")
    require(c6["c6_scientific_verdict"] == "VERIFIED", "C6 result changed")
    require(c6["independent_exact_fraction_cases_passing"] == 112, "C6 exact cases changed")

    required_paths = manifest["required_paths"]
    missing = [path for path in required_paths if not (ROOT / path).exists()]
    require(not missing, f"manifest paths missing: {missing}")
    require(state["canonical_identity"]["email"] == CANONICAL_EMAIL, "state identity mismatch")

    readme = (ROOT / "README.md").read_text()
    for required_text in (
        "arXiv:2509.04477",
        "STATUS.md",
        "CLAIM_EVIDENCE.md",
        "Thank you",
        "not a new judge result",
    ):
        require(required_text in readme, f"README is missing {required_text!r}")

    branch_audit = (ROOT / "branch-audit.md").read_text()
    require(
        f"{CANONICAL_NAME} <{CANONICAL_EMAIL}>" in branch_audit,
        "branch audit identity is not canonical",
    )

    print(
        "FINAL_AUDIT=VERIFIED branches=9 commits=26 "
        "claims=C1_C5_C6_verified_scoped,C2_blocked,C3:C4_falsified_scoped "
        "historical_score=5/12 current_score_claim=false publication_allowed=false"
    )


if __name__ == "__main__":
    main()

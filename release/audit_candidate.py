"""Evaluator-visible release audit.

Run from the root of a fresh clone of the exact candidate Space revision.
This script uses only files reachable from canonical logbook entrypoints and
exits nonzero on any missing visibility, preservation, hash, or secret gate.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path.cwd()
SOURCE_HASH = "238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a"
FIXED_COMMAND = "uv run --frozen python repro/src/verify.py"
CLAIMS = range(1, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def walk_logbook(node: dict, opened: list[str]) -> None:
    path = ROOT / node["file"]
    require(path.is_file(), f"missing logbook page: {node['file']}")
    opened.append(node["file"])
    for child in node.get("children", []):
        walk_logbook(child, opened)


def parse_manifest(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        digest, name = line.split(maxsplit=1)
        rows[name.strip()] = digest
    return rows


def main() -> int:
    opened = ["README.md", "logbook.json"]
    require((ROOT / "README.md").is_file(), "README missing")
    logbook = json.loads((ROOT / "logbook.json").read_text(encoding="utf-8"))
    require(logbook["space_id"] == "DineshAI/63o9EmYHXt", "wrong Space id")
    require(logbook["root"]["children"][0]["slug"] == "current", "current verifier not first")
    require(
        logbook["root"]["children"][1]["title"] == "Historical rejected baseline",
        "historical verifier lacks exact rejection label",
    )
    walk_logbook(logbook["root"], opened)

    index = (ROOT / "pages/index.md").read_text(encoding="utf-8")
    require("Previous live judged score: 5/12" in index, "baseline score not visible")
    require("7–10/12" in index and "10/12" in index, "forecast not visible")
    require(FIXED_COMMAND in index, "fixed command not visible at entrypoint")

    for claim in CLAIMS:
        page_name = f"pages/current/claim-{claim}/page.md"
        page = (ROOT / page_name).read_text(encoding="utf-8")
        require(SOURCE_HASH in page, f"C{claim} source hash missing")
        require(FIXED_COMMAND in page, f"C{claim} fixed command missing")
        require("Reviewer verdict" in page, f"C{claim} verdict missing")
        require("Executable" in page, f"C{claim} code link missing")
        require("Raw" in page or "route summary" in page, f"C{claim} raw link missing")
        require("control" in page.lower(), f"C{claim} control missing")
        require("Git SHA" in page, f"C{claim} Git SHA missing")
        require("cpu-upgrade" in page, f"C{claim} CPU allocation missing")

        claim_dir = ROOT / f"evidence/claims/c{claim}"
        for required in ("claim_contract.json", "source_audit.md", "method.md", "EVAL.md"):
            require((claim_dir / required).is_file(), f"C{claim} missing {required}")
        raw = list(claim_dir.glob("raw_run_*.json"))
        require(len(raw) == 1, f"C{claim} expected one canonical raw JSON")
        json.loads(raw[0].read_text(encoding="utf-8"))
        json.loads((claim_dir / "claim_contract.json").read_text(encoding="utf-8"))
        opened.extend(
            [
                page_name,
                str(raw[0].relative_to(ROOT)),
                f"evidence/claims/c{claim}/claim_contract.json",
                f"evidence/claims/c{claim}/source_audit.md",
                f"evidence/claims/c{claim}/method.md",
                f"evidence/claims/c{claim}/EVAL.md",
            ]
        )

    for source in sorted((ROOT / "repro/src").glob("*.py")):
        ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        opened.append(str(source.relative_to(ROOT)))

    report = (ROOT / "reports/reproduction/report.md").read_text(encoding="utf-8")
    image_links = re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", report)
    require(len(image_links) == 5, "report must expose exactly five evidence figures")
    for relative in image_links:
        image = ROOT / "reports/reproduction" / relative
        require(image.is_file(), f"missing report image: {relative}")
        require("<svg" in image.read_text(encoding="utf-8"), f"not text SVG: {relative}")
        opened.append(str(image.relative_to(ROOT)))
    opened.extend(["reports/reproduction/report.md", "reports/reproduction/release_report.md"])

    historical_manifest = parse_manifest(
        ROOT / "evidence/provenance/judged_space_90cdeab_manifest.sha256"
    )
    for old_path in historical_manifest:
        require((ROOT / old_path).exists(), f"judged file missing from candidate: {old_path}")
    for immutable_page in ("pages/overview/page.md", "pages/verify/page.md"):
        require(
            sha256(ROOT / immutable_page) == historical_manifest[immutable_page],
            f"historical page modified: {immutable_page}",
        )

    allowlist_path = ROOT / "release/upload_allowlist.txt"
    require(allowlist_path.is_file(), "upload allowlist missing")
    allowlist = [
        line for line in allowlist_path.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#")
    ]
    require(len(allowlist) == len(set(allowlist)), "duplicate allowlist path")
    manifest = parse_manifest(ROOT / "release/upload_manifest.sha256")
    for relative in allowlist:
        path = ROOT / relative
        require(path.is_file(), f"allowlisted file missing: {relative}")
        require(b"\0" not in path.read_bytes(), f"non-text file allowlisted: {relative}")
        if relative != "release/upload_manifest.sha256":
            require(manifest.get(relative) == sha256(path), f"manifest mismatch: {relative}")

    secret_patterns = [
        re.compile(r"hf_[A-Za-z0-9]{20,}"),
        re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
        re.compile(r"sk-[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"(?:HF_TOKEN|GITHUB_TOKEN)\s*=\s*\S+"),
    ]
    for relative in allowlist:
        text = (ROOT / relative).read_text(encoding="utf-8")
        require(
            not any(pattern.search(text) for pattern in secret_patterns),
            f"possible secret in {relative}",
        )

    print(
        json.dumps(
            {
                "audit": "PASS",
                "space_id": logbook["space_id"],
                "claims_complete": 6,
                "logbook_pages_opened": len(set(opened)),
                "historical_files_present": len(historical_manifest),
                "historical_pages_byte_identical": True,
                "allowlisted_text_files": len(allowlist),
                "report_figures": len(image_links),
                "fixed_command": FIXED_COMMAND,
                "secrets_detected": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"RELEASE_AUDIT=FAIL: {error}", file=sys.stderr)
        raise

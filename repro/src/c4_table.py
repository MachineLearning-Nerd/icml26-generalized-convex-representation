"""Exact-decimal audit of the live Claim 4 wording against v1 Table I."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path


SOURCE_SHA256 = "238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a"


def audit_c4(table_path: Path) -> dict:
    with table_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    audited = []
    for row in rows:
        n = int(row["number_of_items"])
        learned = Decimal(row["mean_profit_per_item"])
        benchmark_text = row["sja_revenue_per_item"]
        benchmark = None if benchmark_text == "NA" else Decimal(benchmark_text)
        audited.append(
            {
                "n": n,
                "learned_per_item": str(learned),
                "sja_per_item": None if benchmark is None else str(benchmark),
                "exact_equal_at_reported_precision": (
                    None if benchmark is None else learned == benchmark
                ),
                "signed_difference": (
                    None if benchmark is None else str(learned - benchmark)
                ),
            }
        )

    compared = [row for row in audited if row["n"] <= 10]
    mismatch_dimensions = [
        row["n"] for row in compared if not row["exact_equal_at_reported_precision"]
    ]

    # Independent integer arithmetic at the table's three-decimal precision.
    integer_rows = []
    for row in rows:
        n = int(row["number_of_items"])
        if n > 10:
            continue
        learned_milli = int(Decimal(row["mean_profit_per_item"]) * 1000)
        benchmark_milli = int(Decimal(row["sja_revenue_per_item"]) * 1000)
        integer_rows.append(
            {
                "n": n,
                "learned_milli": learned_milli,
                "benchmark_milli": benchmark_milli,
                "difference_milli": learned_milli - benchmark_milli,
            }
        )
    independent_mismatches = [
        row["n"] for row in integer_rows if row["difference_milli"] != 0
    ]

    # This deliberately weakened predicate passes the mismatches and therefore
    # must not be accepted as evidence for the literal word "exactly".
    tolerance_control = all(
        abs(row["learned_milli"] - row["benchmark_milli"]) <= 1
        for row in integer_rows
    )
    exact_match_claim_false = mismatch_dimensions == [5, 10]
    verifier_passed = (
        exact_match_claim_false
        and independent_mismatches == mismatch_dimensions
        and tolerance_control
    )
    return {
        "claim_id": "C4",
        "source_sha256": SOURCE_SHA256,
        "source_anchors": ["#S7.T1", "#S7.p6"],
        "live_claim_tested": (
            "For n up to 10, learned per-item revenue matches the "
            "Straight-Jacket benchmark exactly."
        ),
        "paper_wording": "virtually identical",
        "reported_rows": audited,
        "mismatch_dimensions": mismatch_dimensions,
        "independent_integer_checker": integer_rows,
        "negative_control": {
            "corruption": "replace exact equality by absolute tolerance <= 0.001",
            "corrupted_predicate_passes_all_rows": tolerance_control,
            "rejected_for_exact_claim": tolerance_control,
        },
        "verifier_passed": verifier_passed,
        "scientific_verdict": "FALSIFIED" if verifier_passed else "BLOCKED",
        "confidence": "HIGH" if verifier_passed else "LOW",
        "limitations": (
            "This falsifies only the live claim's literal word 'exactly': "
            "Table I differs by 0.001 per item at n=5 and n=10. It does not "
            "falsify the paper's softer phrase 'virtually identical' and is "
            "not a rerun of the 100,000-step auction training."
        ),
    }

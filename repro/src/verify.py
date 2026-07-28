"""Fixed entrypoint for the cumulative reproduction suite.

This baseline intentionally reconstructs the evaluator-visible toy checks.  It
does not promote them to verification of the paper's universal statements.
Children extend this same entrypoint while the OpenResearch command stays fixed.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from pathlib import Path

# The command is fixed across nodes, so enforce the one-core baseline contract
# in code before importing numerical libraries.
for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ[variable] = "1"

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import core
from c1_proof import verify_c1
from c2_audit import audit_c2
from c3_search import search_c3
from c4_table import audit_c4


ROOT = Path(__file__).resolve().parents[2]
START = time.perf_counter()
SEEDS = {"lean_probe": 2, "ot": 7}


def historical_checks() -> dict:
    x = np.linspace(-4.0, 4.0, 120)
    y = np.linspace(-4.0, 4.0, 120)
    phi = core.phi_matrix(x, y)
    support_counts = [4, 8, 16, 32, 64]

    c1_functions = []
    for name, values in [
        ("x^2/2", x**2 / 2),
        ("(x-1)^2/2", (x - 1) ** 2 / 2),
        ("x^2/2+0.5x", x**2 / 2 + 0.5 * x),
    ]:
        c1_functions.append(
            {
                "function": name,
                "grid_y_convex": core.is_y_convex(values, phi),
                "sup_errors_by_support_count": dict(
                    zip(support_counts, core.denseness_errors(values, phi, support_counts))
                ),
            }
        )

    c2_functions = []
    for name, values in [
        ("x^2/2", x**2 / 2),
        ("x^2/2+0.5x", x**2 / 2 + 0.5 * x),
    ]:
        c2_functions.append(
            {
                "function": name,
                "l1_gradient_errors_by_support_count": dict(
                    zip(support_counts, core.gradient_errors(values, x, phi, support_counts))
                ),
            }
        )

    lean_ok, lean_total = core.lean_convex_combination_probe(seed=SEEDS["lean_probe"])

    price, revenue = core.optimal_posted_price()

    rng = np.random.default_rng(SEEDS["ot"])
    ot_instances = []
    for _ in range(6):
        source = rng.dirichlet(rng.uniform(0.5, 3.0, 80))
        target = rng.dirichlet(rng.uniform(0.5, 3.0, 80))
        ox, potential, transport = core.ot_1d_quadratic(source, target)
        ot_instances.append(
            {
                "brenier_gradient_l1_error": core.brenier_gradient_error(potential, ox, transport),
                "transport_monotone": core.monotone_transport(transport),
            }
        )

    return {
        "artifact_label": "Historical rejected baseline",
        "scientific_scope": "toy finite-grid reconstruction only",
        "claim_statuses": {
            "C1": "BLOCKED",
            "C2": "BLOCKED",
            "C3": "BLOCKED",
            "C4": "BLOCKED",
            "C5": "BLOCKED",
            "C6": "BLOCKED",
        },
        "judge_mapping": {
            "C1": "TOY",
            "C2": "TOY",
            "C3": "TOY",
            "C4": "INCONCLUSIVE",
            "C5": "TOY",
            "C6": "TOY",
        },
        "C1": {
            "domain": "1D [-4,4], 120 points",
            "functions": c1_functions,
        },
        "C2": {
            "domain": "1D [-4,4], 120 points",
            "functions": c2_functions,
        },
        "C3": {
            "convex_combinations_passing_grid_probe": f"{lean_ok}/{lean_total}",
        },
        "C4": {
            "attempted_dimensions": [1],
            "deferred_dimensions": [2, 5, 10, 20],
        },
        "C5": {
            "closed_form_posted_price": price,
            "closed_form_revenue": revenue,
            "two_item_mechanism_run": False,
        },
        "C6": {
            "setting": "six random 1D, 80-bin, quadratic-cost instances",
            "instances": ot_instances,
        },
    }


def regression_passes(result: dict) -> bool:
    c1 = all(row["grid_y_convex"] for row in result["C1"]["functions"])
    c1 = c1 and all(
        list(row["sup_errors_by_support_count"].values())[-1]
        < list(row["sup_errors_by_support_count"].values())[0]
        for row in result["C1"]["functions"]
    )
    c2 = all(
        list(row["l1_gradient_errors_by_support_count"].values())[-1]
        < list(row["l1_gradient_errors_by_support_count"].values())[0]
        for row in result["C2"]["functions"]
    )
    c3 = result["C3"]["convex_combinations_passing_grid_probe"] == "80/80"
    c5 = abs(result["C5"]["closed_form_posted_price"] - 0.5) < 1e-12
    c6 = all(row["transport_monotone"] for row in result["C6"]["instances"])
    honest = set(result["claim_statuses"].values()) == {"BLOCKED"}
    return c1 and c2 and c3 and c5 and c6 and honest


def main() -> int:
    result = historical_checks()
    baseline_regression = regression_passes(result)
    c1 = verify_c1(ROOT / ".openresearch/artifacts/claims/c1/proof_certificate.json")
    c2 = audit_c2()
    c3 = search_c3()
    c4 = audit_c4(ROOT / ".openresearch/artifacts/claims/c4/table_i.csv")
    result["C1_current"] = c1
    result["C2_current"] = c2
    result["C3_current"] = c3
    result["C4_current"] = c4
    result["claim_statuses"]["C1"] = c1["scientific_verdict"]
    result["claim_statuses"]["C2"] = c2["scientific_verdict"]
    result["claim_statuses"]["C3"] = c3["scientific_verdict"]
    result["claim_statuses"]["C4"] = c4["scientific_verdict"]
    result["environment"] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "cpu_count_visible": os.cpu_count(),
        "requested_threads": 1,
    }
    result["runtime_seconds"] = time.perf_counter() - START
    result["historical_regression_passed"] = baseline_regression
    result["historical_expected_result"] = "FAIL"
    print(json.dumps(result, indent=2, sort_keys=True))
    print(
        "HISTORICAL_REJECTED_BASELINE=REPRODUCED"
        if not baseline_regression
        else "HISTORICAL_REJECTED_BASELINE=UNEXPECTED_PASS"
    )
    print(f"C1_SCIENTIFIC_VERDICT={c1['scientific_verdict']}")
    print(f"C2_SCIENTIFIC_VERDICT={c2['scientific_verdict']}")
    print(f"C3_SCIENTIFIC_VERDICT={c3['scientific_verdict']}")
    print(f"C4_SCIENTIFIC_VERDICT={c4['scientific_verdict']}")
    cumulative_passed = (
        (not baseline_regression)
        and c1["verifier_passed"]
        and c2["audit_verifier_passed"]
        and c2["route_protocol_complete"]
        and c3["verifier_passed"]
        and c4["verifier_passed"]
    )
    print("CUMULATIVE_VERIFIER=PASS" if cumulative_passed else "CUMULATIVE_VERIFIER=FAIL")
    return 0 if cumulative_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

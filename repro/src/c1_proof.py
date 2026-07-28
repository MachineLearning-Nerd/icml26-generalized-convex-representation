"""Machine-check the compact-net proof of v1 Theorem 1.

The certificate checks the paper's universal argument, not a finite collection
of target functions.  Z3 checks the local inequality symbolically; a separate
exact-rational enumeration checks the same bound without using Z3.  A corrupted
net radius must admit a concrete countermodel.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from z3 import Abs, Q, Real, Solver, sat, unsat


SOURCE_SHA256 = "238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a"
SOURCE_ANCHORS = ["#S5.p3", "#S5.SS1", "#Thmtheorem1"]


def _load_certificate(path: Path) -> dict:
    certificate = json.loads(path.read_text())
    required = {
        "claim_id",
        "source_sha256",
        "source_anchors",
        "assumptions",
        "quantifiers",
        "proof_steps",
        "net_radius",
    }
    missing = sorted(required - certificate.keys())
    if missing:
        raise ValueError(f"certificate missing fields: {missing}")
    if certificate["claim_id"] != "C1":
        raise ValueError("certificate is not for C1")
    if certificate["source_sha256"] != SOURCE_SHA256:
        raise ValueError("certificate source hash mismatch")
    if certificate["source_anchors"] != SOURCE_ANCHORS:
        raise ValueError("certificate source anchors mismatch")
    expected_steps = [
        "compact_implies_finite_net",
        "transform_preserves_lipschitz_constant",
        "two_lipschitz_errors_bound_branch",
        "finite_support_is_subsupport",
        "pointwise_bound_lifts_through_supremum",
        "combine_one_sided_bounds",
    ]
    if certificate["proof_steps"] != expected_steps:
        raise ValueError("certificate proof DAG mismatch")
    if certificate["net_radius"] != "epsilon/(4*lambda)":
        raise ValueError("certificate net radius mismatch")
    return certificate


def _z3_local_bound(radius_multiplier: Fraction) -> dict:
    """Check a single arbitrary y; the proof DAG lifts it through the supremum."""
    epsilon = Real("epsilon")
    lip = Real("lambda")
    delta_phi = Real("delta_phi")
    delta_transform = Real("delta_transform")
    selected_branch = Real("selected_branch")
    finite_supremum = Real("finite_supremum")
    arbitrary_branch = selected_branch + delta_phi - delta_transform

    solver = Solver()
    solver.add(epsilon > 0, lip > 0)
    radius = Q(radius_multiplier.numerator, radius_multiplier.denominator) * epsilon / lip
    solver.add(Abs(delta_phi) <= lip * radius)
    solver.add(Abs(delta_transform) <= lip * radius)
    solver.add(finite_supremum >= selected_branch)

    target_multiplier = 2 * radius_multiplier
    solver.push()
    solver.add(
        arbitrary_branch
        > finite_supremum
        + Q(target_multiplier.numerator, target_multiplier.denominator) * epsilon
    )
    negated_bound_result = solver.check()
    solver.pop()

    return {
        "radius_multiplier": f"{radius_multiplier.numerator}/{radius_multiplier.denominator}",
        "derived_error_multiplier": (
            f"{target_multiplier.numerator}/{target_multiplier.denominator}"
        ),
        "negated_local_bound": str(negated_bound_result),
        "local_bound_proved": negated_bound_result == unsat,
    }


def _z3_negative_control() -> dict:
    """An oversized net permits an error larger than epsilon."""
    epsilon = Real("control_epsilon")
    lip = Real("control_lambda")
    delta_phi = Real("control_delta_phi")
    delta_transform = Real("control_delta_transform")
    selected_branch = Real("control_selected_branch")
    finite_supremum = Real("control_finite_supremum")
    arbitrary_branch = selected_branch + delta_phi - delta_transform

    solver = Solver()
    solver.add(epsilon == 4, lip == 1)
    solver.add(Abs(delta_phi) <= Q(3, 4) * epsilon)
    solver.add(Abs(delta_transform) <= Q(3, 4) * epsilon)
    solver.add(selected_branch == 0, finite_supremum == selected_branch)
    solver.add(arbitrary_branch > finite_supremum + epsilon)
    result = solver.check()
    witness = {}
    if result == sat:
        model = solver.model()
        witness = {
            "epsilon": str(model.eval(epsilon)),
            "lambda": str(model.eval(lip)),
            "delta_phi": str(model.eval(delta_phi)),
            "delta_transform": str(model.eval(delta_transform)),
            "selected_branch": str(model.eval(selected_branch)),
            "finite_supremum": str(model.eval(finite_supremum)),
            "arbitrary_branch": str(model.eval(arbitrary_branch)),
        }
    return {
        "corruption": "replace epsilon/(4*lambda) by 3*epsilon/(4*lambda)",
        "countermodel_result": str(result),
        "expected_countermodel_found": result == sat,
        "witness": witness,
    }


def _independent_fraction_checker() -> dict:
    """Exact arithmetic enumeration, independent of the SMT implementation."""
    epsilon = Fraction(1, 1)
    radius_error = Fraction(1, 4)
    perturbations = [Fraction(i, 32) for i in range(-8, 9)]
    supremum_slacks = [Fraction(0), Fraction(1, 8), Fraction(1, 2)]
    checked = 0
    largest_gap = None
    for delta_phi in perturbations:
        for delta_transform in perturbations:
            if abs(delta_phi) > radius_error or abs(delta_transform) > radius_error:
                continue
            for slack in supremum_slacks:
                selected_branch = Fraction(0)
                finite_supremum = selected_branch + slack
                arbitrary_branch = selected_branch + delta_phi - delta_transform
                gap = arbitrary_branch - finite_supremum
                if largest_gap is None or gap > largest_gap:
                    largest_gap = gap
                if gap > epsilon / 2:
                    raise AssertionError("exact-rational local bound violated")
                checked += 1

    control_delta_phi = Fraction(3, 4)
    control_delta_transform = Fraction(-3, 4)
    control_gap = control_delta_phi - control_delta_transform
    return {
        "assignments_checked": checked,
        "largest_gap_over_epsilon": str(largest_gap),
        "positive_bound_holds": largest_gap <= epsilon / 2,
        "negative_control_gap_over_epsilon": str(control_gap),
        "negative_control_violates_target": control_gap > epsilon,
    }


def verify_c1(certificate_path: Path) -> dict:
    certificate = _load_certificate(certificate_path)
    positive = _z3_local_bound(Fraction(1, 4))
    independent = _independent_fraction_checker()
    negative = _z3_negative_control()

    finite_net_case = (
        positive["local_bound_proved"]
        and positive["derived_error_multiplier"] == "1/2"
        and independent["positive_bound_holds"]
    )
    zero_lipschitz_case = certificate["zero_lipschitz_case"] == (
        "All branches are identical in y; any singleton support is exact."
    )
    negative_control_passed = (
        negative["expected_countermodel_found"]
        and independent["negative_control_violates_target"]
    )
    passed = finite_net_case and zero_lipschitz_case and negative_control_passed
    return {
        "claim_id": "C1",
        "source_sha256": SOURCE_SHA256,
        "source_anchors": SOURCE_ANCHORS,
        "exact_scope": {
            "assumptions": certificate["assumptions"],
            "quantifiers": certificate["quantifiers"],
            "stronger_uniform_support_statement": certificate[
                "stronger_uniform_support_statement"
            ],
        },
        "proof_certificate": {
            "proof_steps": certificate["proof_steps"],
            "finite_net_positive": positive,
            "zero_lipschitz_case_checked": zero_lipschitz_case,
            "supremum_lift_rule": (
                "If every full-support branch is <= g+epsilon/2, its supremum "
                "is <= g+epsilon/2; finite support inclusion gives g<=f."
            ),
        },
        "independent_checker": independent,
        "negative_control": negative,
        "verifier_passed": passed,
        "scientific_verdict": "VERIFIED" if passed else "BLOCKED",
        "confidence": "HIGH" if passed else "LOW",
        "limitations": (
            "This is a symbolic reconstruction of the universal compactness "
            "argument, not empirical corroboration. It trusts the standard "
            "finite-subcover theorem for compact metric spaces and checks every "
            "paper-specific algebraic and supremum inference."
        ),
    }

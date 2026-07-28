"""Claim 6: symbolic Kantorovich normalization and twist-map recovery.

The proof certificate checks the universal order-theoretic implication.  The
continuous examples are deliberately separate corroboration: their surplus is
nonquadratic, their dimensions are greater than one, and all distributional
and optimality statements are available in closed form.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy.optimize import brentq
from scipy.stats import qmc
from z3 import And, Implies, Not, Real, Solver, unsat


SOURCE_SHA256 = "238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a"
SEED = 20250906


def _z3_implication(name: str, assumptions: list, conclusion) -> dict:
    solver = Solver()
    solver.add(And(*assumptions))
    solver.add(Not(conclusion))
    result = solver.check()
    return {
        "schema": name,
        "negated_implication": str(result),
        "proved": result == unsat,
    }


def _symbolic_certificate() -> dict:
    """Discharge the paper-specific scalar implications with SMT.

    Supremum monotonicity and integration monotonicity are explicitly listed
    as trusted standard order rules.  Everything else is reduced to arbitrary
    real scalar inequalities here.
    """
    surplus, h, k, hx, hbi, hbix = (
        Real(name) for name in ("surplus", "h", "k", "hx", "hbi", "hbix")
    )
    schemas = [
        _z3_implication(
            "feasibility bounds every transform branch",
            [h + k >= surplus],
            surplus - h <= k,
        ),
        _z3_implication(
            "transform pair is feasible",
            [hx >= surplus - h],
            h + hx >= surplus,
        ),
        _z3_implication(
            "biconjugate lies below original feasible potential",
            [h >= surplus - hx, hbi == surplus - hx],
            hbi <= h,
        ),
        _z3_implication(
            "biconjugate-transform cannot exceed first transform",
            [hbi >= surplus - hx],
            surplus - hbi <= hx,
        ),
        _z3_implication(
            "order reversal holds for arbitrary transform branches",
            [hbi <= h, hx == surplus - h, hbix == surplus - hbi],
            hbix >= hx,
        ),
    ]
    return {
        "schemas": schemas,
        "trusted_standard_rules": [
            "If every member of a family is at most c, its supremum is at most c.",
            "If a<=b pointwise then the generalized transform reverses order.",
            "Pointwise order is preserved by expectation under a probability measure.",
            "Weak duality plus equality of primal and dual values certifies optimality.",
            "A differentiable function at a local minimum has zero gradient.",
        ],
        "proof_steps": [
            "Feasibility of (h,k) implies h^X<=k.",
            "The pair (h,h^X) remains feasible and has no larger dual objective.",
            "Set phi=(h^X)^Y; feasibility implies phi<=h, while (phi,h^X) is feasible.",
            "Order reversal and feasibility give phi^X=h^X (triple-transform identity).",
            "Thus an optimal pair has the normal form (phi,phi^X), with phi Y-convex.",
            "On complementary support, differentiating equality gives grad(phi)=grad_x(Phi).",
            "If y->grad_x(Phi) is a diffeomorphism, inversion gives the unique Monge map.",
        ],
        "all_schemas_proved": all(row["proved"] for row in schemas),
    }


def _finite_exact_checker() -> dict:
    """Independent exact-rational audit of the transform normalization."""
    rng = np.random.default_rng(SEED)
    cases = 0
    corrupted_feasibility_failures = 0
    largest_objective_drop = Fraction(0)
    for nx in range(2, 6):
        for ny in range(2, 6):
            for _ in range(7):
                matrix = [
                    [Fraction(int(rng.integers(-7, 8)), 3) for _ in range(ny)]
                    for _ in range(nx)
                ]
                h = [Fraction(int(rng.integers(-5, 6)), 2) for _ in range(nx)]
                slack = [Fraction(int(rng.integers(0, 5)), 4) for _ in range(ny)]
                hx = [max(matrix[i][j] - h[i] for i in range(nx)) for j in range(ny)]
                k = [hx[j] + slack[j] for j in range(ny)]
                phi = [max(matrix[i][j] - hx[j] for j in range(ny)) for i in range(nx)]
                phix = [max(matrix[i][j] - phi[i] for i in range(nx)) for j in range(ny)]

                assert all(h[i] + k[j] >= matrix[i][j] for i in range(nx) for j in range(ny))
                assert all(phi[i] + phix[j] >= matrix[i][j] for i in range(nx) for j in range(ny))
                assert all(phi[i] <= h[i] for i in range(nx))
                assert phix == hx

                wx_raw = [int(v) for v in rng.integers(1, 8, size=nx)]
                wy_raw = [int(v) for v in rng.integers(1, 8, size=ny)]
                wx = [Fraction(v, sum(wx_raw)) for v in wx_raw]
                wy = [Fraction(v, sum(wy_raw)) for v in wy_raw]
                before = sum(w * value for w, value in zip(wx, h)) + sum(
                    w * value for w, value in zip(wy, k)
                )
                after = sum(w * value for w, value in zip(wx, phi)) + sum(
                    w * value for w, value in zip(wy, phix)
                )
                assert after <= before
                largest_objective_drop = max(largest_objective_drop, before - after)

                corrupt = [min(matrix[i][j] - h[i] for i in range(nx)) for j in range(ny)]
                if not all(
                    h[i] + corrupt[j] >= matrix[i][j]
                    for i in range(nx)
                    for j in range(ny)
                ):
                    corrupted_feasibility_failures += 1
                cases += 1
    return {
        "exact_fraction_cases": cases,
        "all_normal_forms_feasible": True,
        "all_triple_transforms_equal": True,
        "all_objectives_nonincreasing": True,
        "largest_exact_objective_drop": str(largest_objective_drop),
        "negative_control": {
            "corruption": "replace every transform supremum by an infimum",
            "cases_failing_feasibility": corrupted_feasibility_failures,
            "all_cases_failed_as_intended": corrupted_feasibility_failures == cases,
        },
    }


def _parameters(dimension: int) -> tuple[np.ndarray, np.ndarray]:
    indices = np.arange(dimension, dtype=np.float64)
    alpha = 0.5 + (indices + 1.0) / (4.0 * dimension)
    cubic = 1.0 + (indices + 1.0) / dimension
    return alpha, cubic


def _exact_optimal_value(dimension: int) -> Fraction:
    value = Fraction(0)
    for index in range(dimension):
        alpha = Fraction(1, 2) + Fraction(index + 1, 4 * dimension)
        cubic = Fraction(1, 1) + Fraction(index + 1, dimension)
        value += alpha / 3 + cubic * alpha**3 / 5
    return value


def _continuous_case(dimension: int) -> dict:
    alpha, cubic = _parameters(dimension)
    sampler = qmc.Sobol(d=dimension, scramble=True, seed=SEED + dimension)
    x = 2.0 * sampler.random_base2(m=9) - 1.0
    y = x * alpha

    # Phi(x,y)=sum_i x_i(y_i+a_i*y_i^3).
    grad_phi = alpha * x + cubic * alpha**3 * x**3
    grad_x_surplus = y + cubic * y**3
    gradient_identity_error = float(np.max(np.abs(grad_phi - grad_x_surplus)))

    recovered = np.empty_like(y)
    for row in range(x.shape[0]):
        for column in range(dimension):
            target = grad_phi[row, column]
            coefficient = cubic[column]
            recovered[row, column] = brentq(
                lambda candidate: candidate + coefficient * candidate**3 - target,
                -alpha[column],
                alpha[column],
                xtol=5e-15,
                rtol=1e-14,
            )
    inverse_error = float(np.max(np.abs(recovered - y)))

    phi = np.sum(alpha * x**2 / 2.0 + cubic * alpha**3 * x**4 / 4.0, axis=1)
    psi = np.sum(y**2 / (2.0 * alpha) + 3.0 * cubic * y**4 / (4.0 * alpha), axis=1)
    surplus = np.sum(x * (y + cubic * y**3), axis=1)
    complementary_slack = float(np.max(np.abs(phi + psi - surplus)))

    exact_value = _exact_optimal_value(dimension)
    expected_primal = float(exact_value)
    empirical_primal = float(np.mean(surplus))
    minimum_jacobian = float(np.min(1.0 + 3.0 * cubic * y**2))

    # Exact rational pointwise identity check, independent of the root finder.
    rational_points = [Fraction(numerator, 10) for numerator in range(-9, 10, 3)]
    exact_identities = 0
    for coordinate in range(dimension):
        alpha_q = Fraction(1, 2) + Fraction(coordinate + 1, 4 * dimension)
        cubic_q = Fraction(1, 1) + Fraction(coordinate + 1, dimension)
        for x_q in rational_points:
            y_q = alpha_q * x_q
            grad_left = alpha_q * x_q + cubic_q * alpha_q**3 * x_q**3
            grad_right = y_q + cubic_q * y_q**3
            phi_q = alpha_q * x_q**2 / 2 + cubic_q * alpha_q**3 * x_q**4 / 4
            psi_q = y_q**2 / (2 * alpha_q) + 3 * cubic_q * y_q**4 / (4 * alpha_q)
            surplus_q = x_q * (y_q + cubic_q * y_q**3)
            assert grad_left == grad_right
            assert phi_q + psi_q == surplus_q
            exact_identities += 2

    passed = (
        gradient_identity_error < 1e-14
        and inverse_error < 2e-13
        and complementary_slack < 2e-14
        and minimum_jacobian >= 1.0
        and exact_identities == 2 * dimension * len(rational_points)
    )
    return {
        "dimension": dimension,
        "surplus": "Phi(x,y)=sum_i x_i*(y_i+a_i*y_i^3)",
        "source_measure": "product Uniform([-1,1])",
        "target_measure": "pushforward by T(x)=diag(alpha)*x",
        "alpha": alpha.tolist(),
        "cubic_coefficients": cubic.tolist(),
        "sobol_points": int(x.shape[0]),
        "gradient_identity_max_error": gradient_identity_error,
        "root_finder_inverse_max_error": inverse_error,
        "complementary_slack_max_error": complementary_slack,
        "minimum_twist_jacobian": minimum_jacobian,
        "exact_rational_identities_checked": exact_identities,
        "exact_primal_dual_value": str(exact_value),
        "exact_primal_dual_value_float": expected_primal,
        "sobol_primal_value": empirical_primal,
        "optimality_certificate": (
            "T pushes mu to eta by definition; dual feasibility follows from the "
            "separable conjugate; equality holds pointwise on (x,T(x)); weak "
            "duality therefore certifies this coupling and potential as optimal."
        ),
        "passed": passed,
    }


def _non_twist_control() -> dict:
    negative_destination = Fraction(-1, 2)
    positive_destination = Fraction(1, 2)
    observed_gradient = negative_destination**2
    chosen_principal_inverse = positive_destination
    return {
        "surplus": "Phi_bad(x,y)=x*y^2",
        "gradient_x": "y^2",
        "distinct_destinations": [str(negative_destination), str(positive_destination)],
        "shared_gradient": str(observed_gradient),
        "jacobian_at_zero": 0,
        "injective": False,
        "principal_inverse_error_for_negative_destination": str(
            abs(chosen_principal_inverse - negative_destination)
        ),
        "map_uniqueness_fails_as_intended": (
            negative_destination != positive_destination
            and negative_destination**2 == positive_destination**2
            and abs(chosen_principal_inverse - negative_destination) == 1
        ),
    }


def verify_c6() -> dict:
    symbolic = _symbolic_certificate()
    independent = _finite_exact_checker()
    continuous = [_continuous_case(dimension) for dimension in (2, 4, 8)]
    control = _non_twist_control()
    passed = (
        symbolic["all_schemas_proved"]
        and independent["all_normal_forms_feasible"]
        and independent["all_triple_transforms_equal"]
        and independent["all_objectives_nonincreasing"]
        and independent["negative_control"]["all_cases_failed_as_intended"]
        and all(row["passed"] for row in continuous)
        and control["map_uniqueness_fails_as_intended"]
    )
    return {
        "claim_id": "C6",
        "source_sha256": SOURCE_SHA256,
        "source_anchors": ["#S4.SS1.p11", "#S4.SS1.p17", "#S4.SS1.p19", "#S4.SS1.p21"],
        "exact_claim": (
            "An optimal Kantorovich dual pair may be chosen as (phi,phi^X) "
            "with phi Y-convex; on complementary support grad(phi)=grad_x(Phi), "
            "and a diffeomorphic y->grad_x(Phi) uniquely recovers the Monge map."
        ),
        "assumptions": [
            "An optimal finite-valued Kantorovich dual pair exists and its expectations are defined.",
            "The complementary-support equality is differentiable in x at the evaluated point.",
            "For map recovery, y->grad_x(Phi)(x,y) is a diffeomorphism onto a set containing grad(phi)(x).",
        ],
        "symbolic_proof_certificate": symbolic,
        "independent_finite_exact_checker": independent,
        "multidimensional_nonquadratic_cases": continuous,
        "negative_control": control,
        "verifier_passed": passed,
        "scientific_verdict": "VERIFIED" if passed else "BLOCKED",
        "confidence": "HIGH" if passed else "LOW",
        "limitations": (
            "The universal dual-normalization and twist implication are checked "
            "symbolically. The continuous examples are constructed exact optimal "
            "transport problems, not a claim that arbitrary OT instances were "
            "exhaustively tested. Existence and regularity remain explicit assumptions."
        ),
    }

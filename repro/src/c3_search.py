"""Exact SMT search for v1 Theorem 4 counterexamples."""

from __future__ import annotations

from fractions import Fraction

from z3 import And, Int, Or, Solver, sat, unsat


SOURCE_SHA256 = "238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a"


def _lean_formula(matrix, parameter, nx: int, ny: int):
    return And(
        *[
            Or(
                *[
                    And(
                        *[
                            matrix[i][j] - parameter[j]
                            >= matrix[i][k] - parameter[k]
                            for k in range(ny)
                        ]
                    )
                    for i in range(nx)
                ]
            )
            for j in range(ny)
        ]
    )


def _midpoint_nonlean_formula(matrix, first, second, nx: int, ny: int):
    """Use scores scaled by two to avoid rational SMT variables."""
    return Or(
        *[
            And(
                *[
                    Or(
                        *[
                            2 * matrix[i][k] - first[k] - second[k]
                            > 2 * matrix[i][j] - first[j] - second[j]
                            for k in range(ny)
                            if k != j
                        ]
                    )
                    for i in range(nx)
                ]
            )
            for j in range(ny)
        ]
    )


def _solve(nx: int, ny: int, identical_control: bool = False) -> dict:
    matrix = [[Int(f"a_{i}_{j}") for j in range(ny)] for i in range(nx)]
    first = [Int(f"f_{j}") for j in range(ny)]
    second = [Int(f"g_{j}") for j in range(ny)]
    solver = Solver()
    all_variables = [value for row in matrix for value in row] + first + second
    solver.add(*[And(value >= -4, value <= 4) for value in all_variables])
    solver.add(matrix[0][0] == 0, first[0] == 0, second[0] == 0)
    solver.add(_lean_formula(matrix, first, nx, ny))
    solver.add(_lean_formula(matrix, second, nx, ny))
    solver.add(_midpoint_nonlean_formula(matrix, first, second, nx, ny))
    if identical_control:
        solver.add(*[first[j] == second[j] for j in range(ny)])
    else:
        solver.add(Or(*[first[j] != second[j] for j in range(ny)]))
    result = solver.check()
    payload = {"nx": nx, "ny": ny, "solver_result": str(result)}
    if result == sat:
        model = solver.model()
        payload["matrix"] = [
            [model.eval(matrix[i][j]).as_long() for j in range(ny)]
            for i in range(nx)
        ]
        payload["first"] = [model.eval(value).as_long() for value in first]
        payload["second"] = [model.eval(value).as_long() for value in second]
    return payload


def _scores(matrix: list[list[int]], parameter: list[Fraction]) -> list[list[Fraction]]:
    return [
        [Fraction(matrix[i][j]) - parameter[j] for j in range(len(parameter))]
        for i in range(len(matrix))
    ]


def _independent_lean_check(
    matrix: list[list[int]], parameter: list[Fraction]
) -> tuple[bool, list[int | None]]:
    scores = _scores(matrix, parameter)
    witnesses = []
    for j in range(len(parameter)):
        witness = next(
            (
                i
                for i, row in enumerate(scores)
                if row[j] == max(row)
            ),
            None,
        )
        witnesses.append(witness)
    return all(witness is not None for witness in witnesses), witnesses


def _independent_nonlean_check(
    matrix: list[list[int]], parameter: list[Fraction]
) -> tuple[bool, int | None, list[int]]:
    scores = _scores(matrix, parameter)
    for j in range(len(parameter)):
        dominators = []
        for row in scores:
            dominator = next(
                (k for k, score in enumerate(row) if k != j and score > row[j]),
                None,
            )
            if dominator is None:
                break
            dominators.append(dominator)
        if len(dominators) == len(scores):
            return True, j, dominators
    return False, None, []


def search_c3() -> dict:
    search_attempts = []
    witness = None
    for nx, ny in [(2, 3), (3, 3), (3, 4), (4, 4)]:
        attempt = _solve(nx, ny)
        search_attempts.append(
            {key: value for key, value in attempt.items() if key not in {"matrix", "first", "second"}}
        )
        if attempt["solver_result"] == "sat":
            witness = attempt
            break

    control = _solve(3, 3, identical_control=True)
    control_passed = control["solver_result"] == "unsat"
    if witness is None:
        return {
            "claim_id": "C3",
            "source_sha256": SOURCE_SHA256,
            "search_attempts": search_attempts,
            "identity_negative_control": control,
            "verifier_passed": control_passed,
            "scientific_verdict": "BLOCKED",
            "confidence": "LOW",
            "reason": "No bounded finite-domain counterexample was found.",
        }

    matrix = witness["matrix"]
    first = [Fraction(value) for value in witness["first"]]
    second = [Fraction(value) for value in witness["second"]]
    midpoint = [(a + b) / 2 for a, b in zip(first, second)]
    first_lean, first_witnesses = _independent_lean_check(matrix, first)
    second_lean, second_witnesses = _independent_lean_check(matrix, second)
    midpoint_nonlean, lost_support, dominators = _independent_nonlean_check(
        matrix, midpoint
    )
    max_kernel_gap = max(value for row in matrix for value in row) - min(
        value for row in matrix for value in row
    )
    assumptions = {
        "X": list(range(len(matrix))),
        "Y_tilde": list(range(len(matrix[0]))),
        "X_and_Y_finite_hence_compact": True,
        "suprema_attained": True,
        "Phi_matrix": matrix,
        "finite_domain_lipschitz_constant_upper_bound": max_kernel_gap,
        "Phi_locally_lipschitz_on_X_times_Y": True,
    }
    verified = (
        first_lean
        and second_lean
        and midpoint_nonlean
        and control_passed
    )
    return {
        "claim_id": "C3",
        "source_sha256": SOURCE_SHA256,
        "source_anchors": ["#S5.SS3", "#Thmtheorem3", "#Thmtheorem4"],
        "exact_claim": "The lean parameter subset for fixed finite Y_tilde is convex.",
        "assumption_audit": assumptions,
        "search_attempts": search_attempts,
        "smt_witness": {
            "matrix": matrix,
            "first_parameter": [str(value) for value in first],
            "second_parameter": [str(value) for value in second],
            "midpoint_parameter": [str(value) for value in midpoint],
        },
        "independent_checker": {
            "first_is_lean": first_lean,
            "first_active_row_by_support": first_witnesses,
            "second_is_lean": second_lean,
            "second_active_row_by_support": second_witnesses,
            "midpoint_is_nonlean": midpoint_nonlean,
            "midpoint_lost_support": lost_support,
            "strict_dominator_by_row": dominators,
            "first_scores": [
                [str(value) for value in row] for row in _scores(matrix, first)
            ],
            "second_scores": [
                [str(value) for value in row] for row in _scores(matrix, second)
            ],
            "midpoint_scores": [
                [str(value) for value in row] for row in _scores(matrix, midpoint)
            ],
        },
        "identity_negative_control": {
            "constraint": "first_parameter == second_parameter while both are lean and midpoint is nonlean",
            "solver_result": control["solver_result"],
            "expected_unsat": control_passed,
        },
        "verifier_passed": verified,
        "scientific_verdict": "FALSIFIED" if verified else "BLOCKED",
        "confidence": "HIGH" if verified else "LOW",
        "limitations": (
            "The counterexample uses finite compact subsets and a finite-domain "
            "locally Lipschitz surplus, which are permitted by the v1 global "
            "assumptions. It does not claim failure for bilinear surplus on "
            "convex continuum domains."
        ),
    }

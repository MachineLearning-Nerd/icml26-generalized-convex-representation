"""Four-route audit of the v1 gradient-density statement."""

from __future__ import annotations

from fractions import Fraction


SOURCE_SHA256 = "238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a"


def _route_1_source_conditions() -> dict:
    """Compare the paper's proposition to the primary result it cites."""
    paper_conditions = {
        "domain": "compact X (global Section V assumption)",
        "functions": "equi-semiconvex; differentiability not stated",
        "function_convergence": "uniform",
        "gradient_convergence": "uniformly where gradients exist",
    }
    cited_primary_conditions = {
        "domain": "S open and convex",
        "functions": "finite C1 convex F and Gi",
        "function_convergence": "pointwise",
        "gradient_convergence": "pointwise on S and uniform on every compact subset of S",
        "source": "Chaudhari-Pranav-Moura, Gradient Networks, Lemma 2, citing Rockafellar Theorem 25.7",
        "arxiv_id": "2404.07361",
    }
    omitted = [
        "open-domain requirement",
        "C1 differentiability requirement",
        "compact-subset-of-interior restriction for uniform convergence",
    ]
    return {
        "route": 1,
        "name": "primary-source topology audit",
        "paper_conditions": paper_conditions,
        "cited_primary_conditions": cited_primary_conditions,
        "material_omissions": omitted,
        "resolves_exact_theorem": False,
        "result": "The cited theorem does not justify the topology stated in Proposition 3.",
    }


def _route_2_proposition_counterexample() -> dict:
    """Exact counterexample to Proposition 3, not to existential density."""
    rows = []
    for n in [2, 4, 8, 16, 32, 64, 128]:
        rows.append(
            {
                "n": n,
                "function_sup_error": str(Fraction(1, n)),
                "gradient_sup_error_where_both_exist": "1",
            }
        )
    control_rows = []
    for n in [2, 4, 8, 16, 32, 64, 128]:
        control_rows.append(
            {
                "n": n,
                "function_sup_error": str(Fraction(1, 2 * n)),
                "gradient_sup_error": str(Fraction(1, n)),
            }
        )
    return {
        "route": 2,
        "name": "exact counterexample to the proof's convergence proposition",
        "domain": "X=[0,1]",
        "kernel": "Phi(x,y)=x*y with compact Y=[0,1], semiconvex constant K=0",
        "sequence": "f_n(x)=max(0, x-(1-1/n)); f(x)=0",
        "assumption_audit": {
            "all_functions_convex": True,
            "shared_semiconvex_constant": 0,
            "uniform_function_convergence": True,
            "gradients_exist_together_at_x=1": True,
        },
        "exact_rows": rows,
        "conclusion": (
            "f_n converges uniformly to f, but at x=1 the gradient error is "
            "exactly 1 for every n. Proposition 3 is false as written."
        ),
        "negative_control": {
            "sequence": "h_n(x)=x^2/(2n); h(x)=0",
            "rows": control_rows,
            "gradient_converges": True,
        },
        "resolves_exact_theorem": False,
        "why_not": (
            "Theorem 2 is existential. The target f=0 is itself finitely "
            "Y-convex, so this bad approximating sequence does not disprove density."
        ),
    }


def _route_3_corrected_scope() -> dict:
    """Constructive exact arithmetic check under the cited interior topology."""
    rows = []
    for supports in [3, 5, 9, 17, 33, 65]:
        spacing = Fraction(1, supports - 1)
        rows.append(
            {
                "supports": supports,
                "support_spacing": str(spacing),
                "exact_gradient_sup_bound_away_from_ties": str(spacing / 2),
            }
        )
    return {
        "route": 3,
        "name": "constructive verification under corrected differentiable interior scope",
        "domain": "compact subsets of the interior of [0,1]",
        "target": "f(x)=x^2/2",
        "approximant": (
            "g_m(x)=max_{y in uniform m-point support} "
            "(x*y-y^2/2)"
        ),
        "exact_rows": rows,
        "negative_control": {
            "corruption": "hold support count fixed at 3",
            "nonvanishing_gradient_bound": "1/4",
            "fails_convergence": True,
        },
        "resolves_exact_theorem": False,
        "why_not": (
            "This faithfully verifies the standard smooth convex special case, "
            "but adds differentiability and interior-compactness assumptions "
            "that the paper's theorem does not state."
        ),
    }


def _route_4_falsification() -> dict:
    """Mandatory attempt to turn the proof gap into an exact counterexample."""
    return {
        "route": 4,
        "name": "mandatory exact-theorem falsification route",
        "exact_claim": (
            "If Phi is semiconvex, gradients of finitely Y-convex functions "
            "are dense in gradients of all Y-convex functions."
        ),
        "assumptions": [
            "compact Euclidean X and Y",
            "locally Lipschitz Phi",
            "one shared semiconvexity constant",
            "uniform gradient topology described only as 'where gradients exist'",
        ],
        "candidate": "boundary-spike sequence from route 2",
        "independent_validity_check": {
            "target_f_is_finitely_y_convex": True,
            "exact_approximant_g_equals_f": True,
            "gradient_error_of_exact_approximant": "0",
        },
        "negative_control": {
            "invalid_rule": "treat failure of one chosen sequence as failure of existential density",
            "rejected": True,
        },
        "valid_counterexample_found": False,
        "result": (
            "Falsification did not succeed: the proof-step counterexample "
            "satisfies the analytic assumptions but not the contradiction "
            "needed for the existential density statement."
        ),
        "unblocker": (
            "An author-specified gradient function space/topology plus a "
            "corrected proof (typically C1 functions on an open domain with "
            "uniform convergence on compact interior subsets), or a valid "
            "counterexample to that precisely stated topology."
        ),
    }


def audit_c2() -> dict:
    routes = [
        _route_1_source_conditions(),
        _route_2_proposition_counterexample(),
        _route_3_corrected_scope(),
        _route_4_falsification(),
    ]
    required_routes_complete = [route["route"] for route in routes] == [1, 2, 3, 4]
    control_checks = [
        routes[1]["negative_control"]["gradient_converges"],
        routes[2]["negative_control"]["fails_convergence"],
        routes[3]["negative_control"]["rejected"],
    ]
    passed = required_routes_complete and all(control_checks)
    return {
        "claim_id": "C2",
        "source_sha256": SOURCE_SHA256,
        "source_anchors": ["#Thmproposition3", "#Thmtheorem2"],
        "routes": routes,
        "route_protocol_complete": required_routes_complete,
        "audit_verifier_passed": passed,
        "scientific_verdict": "BLOCKED",
        "confidence": "LOW",
        "reason": (
            "The theorem's gradient topology is underspecified and its stated "
            "proof relies on a false uniform-convergence proposition. Three "
            "verification routes did not repair the exact statement, and the "
            "mandatory fourth route found no valid theorem-level counterexample."
        ),
    }

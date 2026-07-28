"""Continuous-domain recovery of the one- and two-item auction menus."""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import differential_evolution, minimize_scalar


SOURCE_SHA256 = "238da228cfbb14fed2b33b919a294042e79953d3bbae2ca8b8957ac1a716950a"
SEEDS = [20250905, 20250906, 20250907]


def _two_item_revenue(single_price: float, bundle_increment: float) -> float:
    """Exact integral for p1 in [0,1], p2=p1+q, q in [0,p1]."""
    p1 = single_price
    q = bundle_increment
    p2 = p1 + q
    single_region_area = (1.0 - p1) * q
    excluded_triangle_leg = p1 - q
    bundle_region_area = (1.0 - q) ** 2 - 0.5 * excluded_triangle_leg**2
    return 2.0 * p1 * single_region_area + p2 * bundle_region_area


def _recover_two_item_menu() -> list[dict]:
    runs = []
    for seed in SEEDS:
        result = differential_evolution(
            lambda z: -_two_item_revenue(float(z[0]), float(z[0] * z[1])),
            bounds=[(0.0, 1.0), (0.0, 1.0)],
            seed=seed,
            workers=1,
            updating="immediate",
            polish=True,
            tol=1e-12,
            atol=1e-12,
            maxiter=500,
            popsize=20,
        )
        p1 = float(result.x[0])
        q = float(result.x[0] * result.x[1])
        runs.append(
            {
                "seed": seed,
                "single_price": p1,
                "bundle_price": p1 + q,
                "bundle_increment": q,
                "revenue": -float(result.fun),
                "objective_evaluations": int(result.nfev),
                "optimizer_success": bool(result.success),
                "optimizer_message": str(result.message),
            }
        )
    return runs


def _grid_integral(p1: float, p2: float, side: int) -> float:
    """Independent midpoint quadrature of the buyer's four menu choices."""
    coordinates = (np.arange(side, dtype=np.float64) + 0.5) / side
    payments = np.array([0.0, p1, p1, p2], dtype=np.float64)
    total = 0.0
    batch = 100
    for start in range(0, side, batch):
        x1 = coordinates[start : start + batch, None]
        x2 = coordinates[None, :]
        utilities = np.stack(
            [
                np.zeros((x1.shape[0], side), dtype=np.float64),
                np.broadcast_to(x1 - p1, (x1.shape[0], side)),
                np.broadcast_to(x2 - p1, (x1.shape[0], side)),
                x1 + x2 - p2,
            ],
            axis=0,
        )
        choices = np.argmax(utilities, axis=0)
        total += float(payments[choices].sum())
    return total / (side * side)


def verify_c5() -> dict:
    single = minimize_scalar(
        lambda price: -(price * (1.0 - price)),
        bounds=(0.0, 1.0),
        method="bounded",
        options={"xatol": 1e-14},
    )
    recovered = _recover_two_item_menu()

    theoretical_p1 = 2.0 / 3.0
    theoretical_p2 = (4.0 - math.sqrt(2.0)) / 3.0
    theoretical_q = theoretical_p2 - theoretical_p1
    theoretical_revenue = _two_item_revenue(theoretical_p1, theoretical_q)

    best = max(recovered, key=lambda row: row["revenue"])
    quadrature = [
        {
            "side": side,
            "cells": side * side,
            "integrated_revenue": _grid_integral(
                best["single_price"], best["bundle_price"], side
            ),
        }
        for side in [200, 400, 800]
    ]

    separate_revenue = _two_item_revenue(0.5, 0.5)
    pure_bundle_price = math.sqrt(2.0 / 3.0)
    pure_bundle_revenue = pure_bundle_price * (
        1.0 - pure_bundle_price**2 / 2.0
    )
    price_spread = max(row["single_price"] for row in recovered) - min(
        row["single_price"] for row in recovered
    )
    bundle_spread = max(row["bundle_price"] for row in recovered) - min(
        row["bundle_price"] for row in recovered
    )
    revenue_spread = max(row["revenue"] for row in recovered) - min(
        row["revenue"] for row in recovered
    )

    single_pass = (
        single.success
        and abs(float(single.x) - 0.5) < 1e-7
        and abs(-float(single.fun) - 0.25) < 1e-12
    )
    two_item_pass = (
        all(row["optimizer_success"] for row in recovered)
        and abs(best["single_price"] - theoretical_p1) < 2e-6
        and abs(best["bundle_price"] - theoretical_p2) < 2e-6
        and abs(best["revenue"] - theoretical_revenue) < 2e-10
        and price_spread < 5e-6
        and bundle_spread < 5e-6
        and revenue_spread < 1e-10
    )
    integration_pass = abs(
        quadrature[-1]["integrated_revenue"] - theoretical_revenue
    ) < 2e-3
    controls_pass = (
        theoretical_revenue > separate_revenue + 0.003
        and theoretical_revenue > pure_bundle_revenue + 0.003
    )
    mixed_menu = (
        best["bundle_price"] > best["single_price"]
        and best["bundle_price"] < 2.0 * best["single_price"]
    )
    passed = single_pass and two_item_pass and integration_pass and controls_pass and mixed_menu
    return {
        "claim_id": "C5",
        "source_sha256": SOURCE_SHA256,
        "source_anchors": ["#S7.F2", "#S7.F3"],
        "primary_reference": {
            "paper": "Giannakopoulos and Koutsoupias, Duality and Optimality of Auctions for Uniform Distributions",
            "arxiv_id": "1404.2329",
            "one_item_price": "1/2",
            "two_item_single_price": "2/3",
            "two_item_bundle_price": "(4-sqrt(2))/3",
        },
        "one_item": {
            "recovered_price": float(single.x),
            "recovered_revenue": -float(single.fun),
            "benchmark_price": 0.5,
            "benchmark_revenue": 0.25,
            "passed": single_pass,
        },
        "two_item": {
            "parameterization": [
                {"allocation": [0, 0], "price": 0.0},
                {"allocation": [1, 0], "price": "p1"},
                {"allocation": [0, 1], "price": "p1"},
                {"allocation": [1, 1], "price": "p2"},
            ],
            "domain": "continuous Uniform([0,1]^2), integrated analytically",
            "optimization_runs": recovered,
            "uncertainty": {
                "single_price_seed_spread": price_spread,
                "bundle_price_seed_spread": bundle_spread,
                "revenue_seed_spread": revenue_spread,
            },
            "benchmark": {
                "single_price": theoretical_p1,
                "bundle_price": theoretical_p2,
                "total_revenue": theoretical_revenue,
                "paper_rounded_total_revenue": 0.549,
            },
            "independent_midpoint_quadrature": quadrature,
            "mixed_bundling_confirmed": mixed_menu,
            "passed": two_item_pass and integration_pass,
        },
        "negative_controls": {
            "separate_selling_revenue": separate_revenue,
            "pure_bundle_optimal_price": pure_bundle_price,
            "pure_bundle_revenue": pure_bundle_revenue,
            "mixed_revenue_exceeds_each_by_over_0_003": controls_pass,
        },
        "verifier_passed": passed,
        "scientific_verdict": "VERIFIED" if passed else "BLOCKED",
        "confidence": "MEDIUM" if passed else "LOW",
        "limitations": (
            "The continuous objective and finite generalized-convex menu are "
            "faithful, but this clean-room deterministic optimizer replaces "
            "the official 100,000-step Torch training loop. That optimizer "
            "substitution is why confidence is MEDIUM rather than HIGH."
        ),
    }

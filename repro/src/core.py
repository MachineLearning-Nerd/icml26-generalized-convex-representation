"""Small numerical helpers reconstructed from the judged Space's embedded verifier.

The exact judged Space did not contain its imported ``core`` module.  These
implementations reproduce the visible toy checks without treating them as
evidence for the paper's universal claims.
"""

from __future__ import annotations

import numpy as np


def phi_matrix(x: np.ndarray, y: np.ndarray, kind: str = "inner") -> np.ndarray:
    if kind != "inner":
        raise ValueError(f"unsupported historical kernel: {kind}")
    return np.multiply.outer(x, y)


def conjugate(values: np.ndarray, phi: np.ndarray) -> np.ndarray:
    return np.max(phi - values[:, None], axis=0)


def biconjugate(values: np.ndarray, phi: np.ndarray, indices: np.ndarray | None = None) -> np.ndarray:
    dual = conjugate(values, phi)
    if indices is None:
        indices = np.arange(phi.shape[1])
    return np.max(phi[:, indices] - dual[indices][None, :], axis=1)


def is_y_convex(values: np.ndarray, phi: np.ndarray, tol: float = 1e-6) -> bool:
    return bool(np.max(np.abs(values - biconjugate(values, phi))) <= tol)


def spaced_indices(size: int, count: int) -> np.ndarray:
    return np.unique(np.rint(np.linspace(0, size - 1, min(count, size))).astype(int))


def denseness_errors(values: np.ndarray, phi: np.ndarray, support_counts: list[int]) -> list[float]:
    return [
        float(np.max(np.abs(values - biconjugate(values, phi, spaced_indices(phi.shape[1], k)))))
        for k in support_counts
    ]


def gradient_errors(
    values: np.ndarray,
    x: np.ndarray,
    phi: np.ndarray,
    support_counts: list[int],
) -> list[float]:
    target = np.gradient(values, x)
    return [
        float(np.mean(np.abs(np.gradient(biconjugate(values, phi, spaced_indices(phi.shape[1], k)), x) - target)))
        for k in support_counts
    ]


def lean_convex_combination_probe(trials: int = 80, seed: int = 2) -> tuple[int, int]:
    """Reproduce the historical finite-grid convex-combination sanity check."""
    rng = np.random.default_rng(seed)
    x = np.linspace(-4.0, 4.0, 120)
    palette = [
        0.5 * (x - shift) ** 2 + slope * x + offset
        for shift, slope, offset in [(-1.0, -0.2, 0.0), (0.0, 0.0, 0.3), (1.0, 0.4, -0.1)]
    ]
    passed = 0
    for _ in range(trials):
        i, j = rng.choice(len(palette), size=2, replace=False)
        weight = rng.uniform()
        combo = (1.0 - weight) * palette[i] + weight * palette[j]
        if np.all(np.diff(combo, n=2) >= -1e-10):
            passed += 1
    return passed, trials


def optimal_posted_price() -> tuple[float, float]:
    prices = np.linspace(0.0, 1.0, 1001)
    revenue = prices * (1.0 - prices)
    index = int(np.argmax(revenue))
    return float(prices[index]), float(revenue[index])


def ot_1d_quadratic(
    source_weights: np.ndarray,
    target_weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return a monotone discrete quantile map and an integrated convex potential."""
    n = source_weights.size
    x = np.linspace(0.0, 1.0, n)
    source_cdf = np.cumsum(source_weights)
    target_cdf = np.cumsum(target_weights)
    mapped_indices = np.searchsorted(target_cdf, source_cdf, side="left").clip(max=n - 1)
    transport = x[mapped_indices]
    potential = np.zeros_like(x)
    potential[1:] = np.cumsum(0.5 * (transport[1:] + transport[:-1]) * np.diff(x))
    return x, potential, transport


def brenier_gradient_error(potential: np.ndarray, x: np.ndarray, transport: np.ndarray) -> float:
    return float(np.mean(np.abs(np.gradient(potential, x) - transport)))


def monotone_transport(transport: np.ndarray) -> bool:
    return bool(np.all(np.diff(transport) >= -1e-12))

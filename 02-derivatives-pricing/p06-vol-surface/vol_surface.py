"""SVI volatility smiles and arbitrage checks.

params is always a tuple (a, b, rho, m, sigma) for raw SVI:
    w(k) = a + b * (rho * (k - m) + sqrt((k - m)**2 + sigma**2))
All functions should accept numpy arrays for k.
"""
from __future__ import annotations

import numpy as np

SVIParams = tuple[float, float, float, float, float]


def svi_total_variance(k: np.ndarray, params: SVIParams) -> np.ndarray:
    raise NotImplementedError


def svi_derivatives(k: np.ndarray, params: SVIParams) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (w, dw/dk, d2w/dk2), computed analytically."""
    raise NotImplementedError


def butterfly_g(k: np.ndarray, params: SVIParams) -> np.ndarray:
    """Gatheral's g(k) = (1 - k w'/(2w))^2 - (w'^2/4)(1/w + 1/4) + w''/2."""
    raise NotImplementedError


def has_butterfly_arbitrage(params: SVIParams, k_grid: np.ndarray | None = None) -> bool:
    """True if g(k) < 0 anywhere on k_grid (default: np.linspace(-3, 3, 2001)) or w <= 0 anywhere."""
    raise NotImplementedError


def has_calendar_arbitrage(
    slices: list[tuple[float, SVIParams]], k_grid: np.ndarray | None = None
) -> bool:
    """slices: list of (T, params). True if total variance decreases in T at any k on k_grid."""
    raise NotImplementedError


def svi_density(k: np.ndarray, params: SVIParams) -> np.ndarray:
    """Risk-neutral density of log-moneyness k implied by the smile:
        p(k) = g(k) / sqrt(2 pi w(k)) * exp(-d2(k)^2 / 2),   d2 = -k/sqrt(w) - sqrt(w)/2
    """
    raise NotImplementedError


def fit_svi(k: np.ndarray, w: np.ndarray, weights: np.ndarray | None = None) -> SVIParams:
    """Least-squares fit of raw SVI to observed total variances w at log-moneyness k.

    Enforce b >= 0, |rho| < 1, sigma > 0, and a + b * sigma * sqrt(1 - rho^2) >= 0 (w >= 0).
    """
    raise NotImplementedError

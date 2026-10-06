"""Portfolio construction and risk. numpy (+ scipy.stats for quantiles) only."""
from __future__ import annotations

import numpy as np


def min_variance_weights(cov: np.ndarray) -> np.ndarray:
    """argmin w' S w  s.t.  sum(w) = 1  (shorts allowed)."""
    raise NotImplementedError


def mean_variance_weights(mu: np.ndarray, cov: np.ndarray, risk_aversion: float) -> np.ndarray:
    """argmax w' mu - (risk_aversion / 2) w' S w   (unconstrained; the rest is in cash)."""
    raise NotImplementedError


def tangency_weights(mu: np.ndarray, cov: np.ndarray, rf: float = 0.0) -> np.ndarray:
    """Maximum-Sharpe fully-invested portfolio (weights sum to 1)."""
    raise NotImplementedError


def ledoit_wolf(returns: np.ndarray) -> tuple[np.ndarray, float]:
    """Ledoit-Wolf (2004) shrinkage toward F = m I, m = trace(S)/p.

    returns: (T, p) array. Use the *biased* sample covariance S = X'X / T on demeaned X.
    Return (delta F + (1 - delta) S, delta), with the optimal delta clipped to [0, 1]:
        d2 = ||S - F||_F^2 / p
        b2_bar = (1 / T^2) * sum_t ||x_t x_t' - S||_F^2 / p
        b2 = min(b2_bar, d2);  delta = b2 / d2
    (||.||_F is the Frobenius norm; x_t is row t of the demeaned data.)
    """
    raise NotImplementedError


def pca(returns: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """Principal components of the (demeaned) returns.

    Return (loadings, explained_variance_ratio): loadings is (p, k) with orthonormal columns,
    ordered by decreasing variance; explained_variance_ratio has length k.
    """
    raise NotImplementedError


def risk_contributions(w: np.ndarray, cov: np.ndarray) -> np.ndarray:
    """RC_i = w_i (S w)_i / sigma_p, so that sum(RC) == sigma_p."""
    raise NotImplementedError


def risk_parity_weights(cov: np.ndarray, tol: float = 1e-10, max_iter: int = 10_000) -> np.ndarray:
    """Long-only weights (sum to 1) with equal risk contributions.

    Warning: the "obvious" fixed-point iteration w_i <- 1/(S w)_i breaks when some assets are
    negatively correlated ((S w)_i can go negative). Look up Spinu (2013): minimise
    0.5 y'Sy - (1/n) sum(log y_i), which is convex, then normalise y.
    """
    raise NotImplementedError


def historical_var(pnl: np.ndarray, level: float = 0.99) -> float:
    """Historical VaR as a positive loss: -quantile(pnl, 1 - level) (numpy default interpolation)."""
    raise NotImplementedError


def historical_es(pnl: np.ndarray, level: float = 0.99) -> float:
    """Expected shortfall as a positive loss: -mean(pnl[pnl <= -VaR])."""
    raise NotImplementedError


def parametric_var(mu: float, sigma: float, level: float = 0.99) -> float:
    """Normal VaR as a positive loss: -(mu + sigma * z_{1-level})."""
    raise NotImplementedError

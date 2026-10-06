"""Pairs trading toolkit. numpy only (no statsmodels) inside your implementations."""
from __future__ import annotations

import numpy as np


def hedge_ratio_ols(y: np.ndarray, x: np.ndarray) -> tuple[float, float]:
    """OLS of y on [1, x]. Return (alpha, beta)."""
    raise NotImplementedError


def adf_tstat(series: np.ndarray, lags: int = 0) -> float:
    """Augmented Dickey-Fuller t-statistic (with constant, no trend).

    Regress  dy_t = a + g * y_{t-1} + sum_{i=1..lags} phi_i * dy_{t-i} + e_t
    over t = lags+1 .. n-1 (0-indexed on y; dy_t = y_t - y_{t-1}) and return g / se(g),
    using the classical OLS standard error with sigma^2 = RSS / (n_obs - n_params).
    """
    raise NotImplementedError


def engle_granger(y: np.ndarray, x: np.ndarray, lags: int = 0) -> tuple[float, float]:
    """Return (beta, adf_tstat of the OLS residual y - alpha - beta x)."""
    raise NotImplementedError


def fit_ou(series: np.ndarray, dt: float = 1.0) -> dict[str, float]:
    """Fit dX = kappa (mu - X) dt + sigma dW via the exact AR(1) discretisation
        X_{t+1} = a + b X_t + e,  b = exp(-kappa dt),  a = mu (1 - b),
        Var(e) = sigma^2 (1 - b^2) / (2 kappa).
    Estimate a, b by OLS and Var(e) by the residual variance with ddof=2.
    Return {"kappa", "mu", "sigma", "half_life"} with half_life = ln 2 / kappa.
    Raise ValueError if the fitted b is not in (0, 1) (no mean reversion).
    """
    raise NotImplementedError


def zscore_positions(spread: np.ndarray, window: int, entry: float = 2.0, exit: float = 0.5) -> np.ndarray:
    """Hysteresis band rule on a rolling z-score.

    z_t = (spread_t - mean(spread[t-window+1 .. t])) / std(same window, ddof=1); z is undefined
    (position 0) for t < window - 1.
    Position rules, applied sequentially starting flat:
      flat  -> short (-1) if z >  entry;  long (+1) if z < -entry
      short -> flat if z <  exit
      long  -> flat if z > -exit
    (No direct flip from long to short in one step.) Return an int array of positions.
    """
    raise NotImplementedError


def kalman_hedge_ratio(
    y: np.ndarray, x: np.ndarray, delta: float = 1e-4, obs_var: float = 1e-3
) -> tuple[np.ndarray, np.ndarray]:
    """Kalman filter for y_t = alpha_t + beta_t x_t + v_t, with [alpha, beta] a random walk.

    State covariance noise W = delta / (1 - delta) * I, observation noise variance obs_var.
    Start from state [0, 0] with covariance P = 1e3 * I (diffuse prior; the original
    textbook choice of P = 0 is a trap: why?).
    Return (alphas, betas): the *filtered* estimates after observing y_t, each of length n.
    """
    raise NotImplementedError

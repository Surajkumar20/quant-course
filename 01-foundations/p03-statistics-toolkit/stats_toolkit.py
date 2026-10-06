"""Statistics toolkit built from scratch.

Allowed: numpy, scipy.stats distribution functions (cdf/ppf), scipy.optimize.minimize.
Not allowed: statsmodels, sklearn, scipy.stats test functions (ttest_1samp, etc.) inside your
implementations. Use those in your *own* tests to check your answers.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


def mle_normal(x: np.ndarray) -> tuple[float, float]:
    """Return (mu_hat, sigma_hat), the maximum-likelihood estimates."""
    raise NotImplementedError


def mle_exponential(x: np.ndarray) -> float:
    """Return lambda_hat (rate) for an Exponential(rate) sample."""
    raise NotImplementedError


def mle_numeric(
    neg_log_lik: Callable[[np.ndarray], float], x0: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Minimise neg_log_lik starting at x0.

    Return (theta_hat, standard_errors), with standard errors from the inverse Hessian of
    neg_log_lik at theta_hat. Compute the Hessian yourself by central finite differences.
    """
    raise NotImplementedError


def one_sample_t_test(x: np.ndarray, mu0: float = 0.0) -> tuple[float, float]:
    """Return (t_statistic, two_sided_p_value) for H0: mean == mu0."""
    raise NotImplementedError


@dataclass
class OLSResult:
    beta: np.ndarray      # (k,)
    se: np.ndarray        # (k,) classical (homoskedastic) standard errors
    t: np.ndarray         # (k,)
    r2: float
    resid: np.ndarray     # (n,)


def ols(X: np.ndarray, y: np.ndarray, add_intercept: bool = True) -> OLSResult:
    """Ordinary least squares. If add_intercept, prepend a column of ones (beta[0] is the intercept).

    Use sigma^2 = RSS / (n - k) for the standard errors.
    """
    raise NotImplementedError


def newey_west_se(X: np.ndarray, resid: np.ndarray, lags: int) -> np.ndarray:
    """HAC (Newey-West, Bartlett kernel) standard errors.

    X must already include the intercept column if there is one (i.e. the same design matrix
    used for the fit). Use no small-sample correction: S = sum over |l| <= lags of
    w_l * Gamma_l with Gamma_l = (1/n) sum_t u_t u_{t-l} x_t x_{t-l}^T and w_l = 1 - |l|/(lags+1);
    Var(beta) = (1/n) Q^{-1} S Q^{-1}, Q = X^T X / n.
    """
    raise NotImplementedError


def bootstrap_ci(
    x: np.ndarray,
    stat: Callable[[np.ndarray], float],
    n_boot: int,
    level: float,
    rng: np.random.Generator,
) -> tuple[float, float]:
    """Percentile bootstrap confidence interval for stat(x)."""
    raise NotImplementedError


def permutation_test(x: np.ndarray, y: np.ndarray, n_perm: int, rng: np.random.Generator) -> float:
    """Two-sided p-value for H0: mean(x) == mean(y), using |mean(x) - mean(y)| as the statistic.

    Use the (count + 1) / (n_perm + 1) convention so the p-value is never exactly 0.
    """
    raise NotImplementedError


def sharpe_ratio(returns: np.ndarray, periods_per_year: int = 252) -> float:
    """Annualised Sharpe ratio of excess returns: mean/std (ddof=1) * sqrt(periods_per_year)."""
    raise NotImplementedError


def sharpe_se(returns: np.ndarray) -> float:
    """Lo (2002) iid standard error of the *per-period* (non-annualised) Sharpe ratio:
    sqrt((1 + SR^2 / 2) / T).
    """
    raise NotImplementedError

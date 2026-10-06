"""Validation tools for financial ML. numpy + scipy.stats only."""
from __future__ import annotations

import numpy as np


def purged_kfold_splits(
    n: int, n_splits: int, label_horizon: int, embargo: int = 0
) -> list[tuple[np.ndarray, np.ndarray]]:
    """K-fold CV for time-ordered samples whose labels overlap.

    Sample i's label is computed from times [i, i + label_horizon].
    Test folds are contiguous: np.array_split(np.arange(n), n_splits).
    For a test fold covering samples [a, b], the training set is every sample i NOT in
        [a - label_horizon, b + label_horizon + embargo]
    i.e. we purge any training sample whose label window overlaps the test fold's label windows,
    then embargo `embargo` further samples after the test fold.
    Return [(train_idx, test_idx), ...] as sorted int arrays.
    """
    raise NotImplementedError


def walk_forward_splits(
    n: int, train_size: int, test_size: int, gap: int = 0
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Rolling windows: train [s, s+train_size), test [s+train_size+gap, s+train_size+gap+test_size),
    for s = 0, test_size, 2*test_size, ... while the test window fits inside [0, n).
    """
    raise NotImplementedError


def rank_ic(pred: np.ndarray, realized: np.ndarray) -> float:
    """Spearman rank correlation between predictions and realised returns (one cross-section).

    Ignore pairs where either value is NaN. Average ranks for ties.
    """
    raise NotImplementedError


def probabilistic_sharpe_ratio(
    sr: float, sr_benchmark: float, n_obs: int, skew: float = 0.0, kurt: float = 3.0
) -> float:
    """PSR (Bailey & Lopez de Prado). sr and sr_benchmark are *per-period* (not annualised).

    PSR = Phi( (sr - sr_benchmark) * sqrt(n_obs - 1) / sqrt(1 - skew*sr + (kurt - 1)/4 * sr^2) )
    """
    raise NotImplementedError


def expected_max_sharpe(n_trials: int, sr_variance: float) -> float:
    """Expected maximum of n_trials Sharpe ratios drawn with zero mean and variance sr_variance:

    sqrt(V) * ((1 - g) * Phi^-1(1 - 1/N) + g * Phi^-1(1 - 1/(N e))),  g = Euler-Mascheroni.
    Return 0.0 when n_trials == 1.
    """
    raise NotImplementedError


def deflated_sharpe_ratio(
    sr: float, n_trials: int, sr_variance: float, n_obs: int, skew: float = 0.0, kurt: float = 3.0
) -> float:
    """DSR = PSR with the benchmark set to expected_max_sharpe(n_trials, sr_variance)."""
    raise NotImplementedError

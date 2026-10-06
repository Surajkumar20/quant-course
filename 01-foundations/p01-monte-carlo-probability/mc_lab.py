"""Monte Carlo probability lab.

Every simulation takes a `numpy.random.Generator` so results are reproducible.
Don't change function signatures, because the tests depend on them.
"""
from __future__ import annotations

import numpy as np


def mc_mean_ci(samples: np.ndarray, level: float = 0.95) -> tuple[float, float, float]:
    """Return (mean, lo, hi): a CLT confidence interval for the mean of `samples`.

    Use the sample standard deviation (ddof=1) and the normal quantile for `level`.
    """
    raise NotImplementedError


def estimate_pi(n: int, rng: np.random.Generator) -> tuple[float, float]:
    """Estimate pi by throwing n points in the unit square. Return (estimate, standard_error)."""
    raise NotImplementedError


def coupon_collector_expected(n: int) -> float:
    """Exact expected number of draws to see all n equally likely coupons."""
    raise NotImplementedError


def coupon_collector_sim(n: int, n_trials: int, rng: np.random.Generator) -> np.ndarray:
    """Simulate the coupon collector; return an array of length n_trials with the draw counts."""
    raise NotImplementedError


def gamblers_ruin_prob(start: int, target: int, p: float = 0.5) -> float:
    """Exact P(hit `target` before 0) for a walk starting at `start`, stepping +1 w.p. p, else -1."""
    raise NotImplementedError


def gamblers_ruin_sim(start: int, target: int, p: float, n_trials: int, rng: np.random.Generator) -> float:
    """Simulated version of gamblers_ruin_prob."""
    raise NotImplementedError


def walk_max_prob_exact(n_steps: int, level: int) -> float:
    """Exact P(max_{k<=n} S_k >= level) for a simple symmetric +-1 random walk, level >= 1.

    Hint: reflection principle.
    """
    raise NotImplementedError


def walk_max_prob_sim(n_steps: int, level: int, n_paths: int, rng: np.random.Generator) -> float:
    """Vectorised simulation of walk_max_prob_exact (no Python loop over paths)."""
    raise NotImplementedError


def draws_until_sum_exceeds_one(n_trials: int, rng: np.random.Generator) -> np.ndarray:
    """For each trial, count Uniform(0,1) draws until the running sum exceeds 1."""
    raise NotImplementedError

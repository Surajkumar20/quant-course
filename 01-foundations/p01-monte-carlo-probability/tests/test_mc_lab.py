import math

import numpy as np
import pytest

import mc_lab as m


@pytest.fixture
def rng():
    return np.random.default_rng(12345)


def within(estimate, truth, se, k=4.0):
    """Statistical assertion: estimate within k standard errors of the truth."""
    return abs(estimate - truth) <= k * se


# ---- confidence intervals --------------------------------------------------

def test_mc_mean_ci_known_values():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    mean, lo, hi = m.mc_mean_ci(x, 0.95)
    se = np.std(x, ddof=1) / math.sqrt(5)
    assert mean == pytest.approx(3.0)
    assert lo == pytest.approx(3.0 - 1.959963985 * se, rel=1e-6)
    assert hi == pytest.approx(3.0 + 1.959963985 * se, rel=1e-6)


def test_mc_mean_ci_coverage(rng):
    hits = 0
    for _ in range(400):
        _, lo, hi = m.mc_mean_ci(rng.exponential(1.0, size=500), 0.95)
        hits += lo <= 1.0 <= hi
    assert 0.90 <= hits / 400 <= 0.985


# ---- pi ---------------------------------------------------------------------

def test_estimate_pi(rng):
    est, se = m.estimate_pi(200_000, rng)
    assert se == pytest.approx(4 * math.sqrt(math.pi / 4 * (1 - math.pi / 4) / 200_000), rel=0.05)
    assert within(est, math.pi, se)


# ---- coupon collector ---------------------------------------------------------

def test_coupon_collector_expected():
    assert m.coupon_collector_expected(1) == pytest.approx(1.0)
    assert m.coupon_collector_expected(6) == pytest.approx(14.7)
    assert m.coupon_collector_expected(50) == pytest.approx(224.9603, rel=1e-6)


def test_coupon_collector_sim(rng):
    draws = m.coupon_collector_sim(6, 20_000, rng)
    assert draws.shape == (20_000,)
    assert draws.min() >= 6
    se = draws.std(ddof=1) / math.sqrt(len(draws))
    assert within(draws.mean(), 14.7, se)


# ---- gambler's ruin -----------------------------------------------------------

def test_gamblers_ruin_fair():
    assert m.gamblers_ruin_prob(1, 3, 0.5) == pytest.approx(1 / 3)
    assert m.gamblers_ruin_prob(37, 100, 0.5) == pytest.approx(0.37)


def test_gamblers_ruin_biased():
    # q/p = 1.5, start 5, target 10
    r = 0.6 / 0.4
    expected = (1 - r**5) / (1 - r**10)
    assert m.gamblers_ruin_prob(5, 10, 0.4) == pytest.approx(expected)
    # roulette-style: tiny edge against you compounds
    assert m.gamblers_ruin_prob(50, 100, 18 / 38) < 0.01


def test_gamblers_ruin_edges():
    assert m.gamblers_ruin_prob(0, 10, 0.3) == pytest.approx(0.0)
    assert m.gamblers_ruin_prob(10, 10, 0.3) == pytest.approx(1.0)


def test_gamblers_ruin_sim(rng):
    p_hat = m.gamblers_ruin_sim(3, 8, 0.45, 20_000, rng)
    truth = m.gamblers_ruin_prob(3, 8, 0.45)
    assert within(p_hat, truth, math.sqrt(truth * (1 - truth) / 20_000))


# ---- random walk maximum -----------------------------------------------------

def test_walk_max_exact_small_cases():
    assert m.walk_max_prob_exact(1, 1) == pytest.approx(0.5)
    assert m.walk_max_prob_exact(2, 1) == pytest.approx(0.5)  # UU, UD reach +1; DU, DD don't
    assert m.walk_max_prob_exact(3, 1) == pytest.approx(0.625)
    assert m.walk_max_prob_exact(3, 3) == pytest.approx(1 / 8)
    assert m.walk_max_prob_exact(5, 6) == pytest.approx(0.0)


def test_walk_max_exact_matches_bruteforce():
    import itertools

    n, a = 10, 3
    hits = 0
    for steps in itertools.product((-1, 1), repeat=n):
        hits += max(itertools.accumulate(steps)) >= a
    assert m.walk_max_prob_exact(n, a) == pytest.approx(hits / 2**n)


def test_walk_max_sim(rng):
    truth = m.walk_max_prob_exact(100, 10)
    p_hat = m.walk_max_prob_sim(100, 10, 100_000, rng)
    assert within(p_hat, truth, math.sqrt(truth * (1 - truth) / 100_000))


# ---- e ----------------------------------------------------------------------

def test_draws_until_sum_exceeds_one(rng):
    n = m.draws_until_sum_exceeds_one(100_000, rng)
    assert n.shape == (100_000,)
    assert n.min() >= 2
    se = n.std(ddof=1) / math.sqrt(len(n))
    assert within(n.mean(), math.e, se)

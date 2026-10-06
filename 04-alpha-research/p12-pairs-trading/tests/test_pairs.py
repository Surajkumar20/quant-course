import math

import numpy as np
import pytest

import pairs as pt


@pytest.fixture
def rng():
    return np.random.default_rng(7)


def simulate_ou(n, kappa, mu, sigma, rng, x0=None):
    b = math.exp(-kappa)
    sd = sigma * math.sqrt((1 - b * b) / (2 * kappa))
    x = np.empty(n)
    x[0] = mu if x0 is None else x0
    for t in range(1, n):
        x[t] = mu + b * (x[t - 1] - mu) + sd * rng.normal()
    return x


def test_hedge_ratio_ols(rng):
    x = np.cumsum(rng.normal(size=500)) + 100
    y = 3.0 + 1.5 * x + rng.normal(scale=0.1, size=500)
    a, b = pt.hedge_ratio_ols(y, x)
    assert b == pytest.approx(1.5, abs=0.01)
    assert a == pytest.approx(3.0, abs=1.0)


def test_adf_matches_manual_regression(rng):
    y = np.cumsum(rng.normal(size=300))
    dy = np.diff(y)
    # lags = 1: regress dy_t on [1, y_{t-1}, dy_{t-1}] for t = 2..n-1
    Y = dy[1:]
    X = np.column_stack([np.ones(len(Y)), y[1:-1], dy[:-1]])
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid = Y - X @ beta
    s2 = resid @ resid / (len(Y) - 3)
    se = math.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    assert pt.adf_tstat(y, lags=1) == pytest.approx(beta[1] / se)


def test_adf_separates_stationary_from_random_walk(rng):
    stationary = simulate_ou(1000, 0.3, 0.0, 1.0, rng)
    walk = np.cumsum(rng.normal(size=1000))
    assert pt.adf_tstat(stationary) < -5
    assert pt.adf_tstat(walk) > -2.86


def test_engle_granger(rng):
    n = 1500
    x = np.cumsum(rng.normal(size=n)) + 50
    spread = simulate_ou(n, 0.1, 0.0, 0.5, rng)
    y = 2.0 + 0.8 * x + spread
    beta, t = pt.engle_granger(y, x)
    assert beta == pytest.approx(0.8, abs=0.02)
    assert t < -3.34
    z = np.cumsum(rng.normal(size=n)) + 50  # independent walk
    _, t_indep = pt.engle_granger(z, x)
    assert t_indep > -3.34


def test_fit_ou_recovers_parameters(rng):
    x = simulate_ou(20_000, kappa=0.05, mu=1.5, sigma=0.3, rng=rng)
    p = pt.fit_ou(x)
    assert p["kappa"] == pytest.approx(0.05, rel=0.15)
    assert p["mu"] == pytest.approx(1.5, abs=0.1)
    assert p["sigma"] == pytest.approx(0.3, rel=0.05)
    assert p["half_life"] == pytest.approx(math.log(2) / p["kappa"])


def test_fit_ou_rejects_random_walk(rng):
    with pytest.raises(ValueError):
        pt.fit_ou(np.cumsum(np.abs(rng.normal(size=500))))  # trending: b > 1


def test_zscore_positions_hysteresis():
    window = 5
    base = [0.0, 1.0, 0.0, 1.0, 0.0]  # mean 0.4, std ~0.548
    spread = np.array(base + [3.0, 2.0, 0.4, 0.4, -3.0, -1.0, 0.0, 0.0])
    pos = pt.zscore_positions(spread, window, entry=1.5, exit=0.5)
    assert pos.dtype.kind == "i"
    assert len(pos) == len(spread)
    assert list(pos[:4]) == [0, 0, 0, 0]       # warm-up
    assert pos[5] == -1                          # big positive z -> short
    # hand-check by recomputing z
    z = [(spread[t] - spread[t - 4:t + 1].mean()) / spread[t - 4:t + 1].std(ddof=1) for t in range(4, len(spread))]
    state, expect = 0, [0, 0, 0, 0]
    for zt in z:
        if state == 0:
            state = -1 if zt > 1.5 else (1 if zt < -1.5 else 0)
        elif state == -1 and zt < 0.5:
            state = 0
        elif state == 1 and zt > -0.5:
            state = 0
        expect.append(state)
    assert list(pos) == expect
    assert 1 in expect and -1 in expect


def test_kalman_tracks_constant_and_changing_beta(rng):
    n = 2000
    x = np.cumsum(rng.normal(size=n)) + 100
    beta_true = np.where(np.arange(n) < 1000, 0.5, 1.2)
    y = 1.0 + beta_true * x + rng.normal(scale=0.05, size=n)
    alphas, betas = pt.kalman_hedge_ratio(y, x, delta=1e-4, obs_var=0.05**2)
    assert alphas.shape == betas.shape == (n,)
    assert np.mean(betas[800:1000]) == pytest.approx(0.5, abs=0.05)
    assert np.mean(betas[1800:]) == pytest.approx(1.2, abs=0.05)

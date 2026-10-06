import math

import numpy as np
import pytest
from scipy import stats

import stats_toolkit as st


@pytest.fixture
def rng():
    return np.random.default_rng(2024)


def test_mle_normal(rng):
    x = rng.normal(3.0, 2.0, size=1000)
    mu, sigma = st.mle_normal(x)
    assert mu == pytest.approx(x.mean())
    assert sigma == pytest.approx(x.std(ddof=0))


def test_mle_exponential(rng):
    x = rng.exponential(1 / 4.0, size=5000)
    assert st.mle_exponential(x) == pytest.approx(1 / x.mean())


def test_mle_numeric_matches_closed_form(rng):
    x = rng.normal(1.0, 0.5, size=2000)

    def nll(theta):
        mu, log_sigma = theta
        s = math.exp(log_sigma)
        return 0.5 * np.sum(((x - mu) / s) ** 2) + len(x) * log_sigma

    theta, se = st.mle_numeric(nll, np.array([0.0, 0.0]))
    assert theta[0] == pytest.approx(x.mean(), abs=1e-4)
    assert math.exp(theta[1]) == pytest.approx(x.std(ddof=0), rel=1e-4)
    # SE(mu_hat) = sigma / sqrt(n); SE(log sigma_hat) = 1/sqrt(2n)
    assert se[0] == pytest.approx(x.std() / math.sqrt(len(x)), rel=0.02)
    assert se[1] == pytest.approx(1 / math.sqrt(2 * len(x)), rel=0.02)


def test_t_test_matches_scipy(rng):
    x = rng.normal(0.1, 1.0, size=50)
    t, p = st.one_sample_t_test(x, 0.0)
    ref = stats.ttest_1samp(x, 0.0)
    assert t == pytest.approx(ref.statistic)
    assert p == pytest.approx(ref.pvalue)


def test_ols_recovers_known_coefficients(rng):
    n = 500
    X = rng.normal(size=(n, 2))
    y = 1.0 + 2.0 * X[:, 0] - 0.5 * X[:, 1] + rng.normal(scale=0.1, size=n)
    res = st.ols(X, y)
    assert res.beta == pytest.approx([1.0, 2.0, -0.5], abs=0.02)
    assert res.r2 > 0.99
    assert res.resid.shape == (n,)
    assert res.t == pytest.approx(res.beta / res.se)


def test_ols_standard_errors_match_formula(rng):
    n = 200
    x = rng.normal(size=n)
    y = 0.3 + 0.7 * x + rng.normal(size=n)
    res = st.ols(x.reshape(-1, 1), y)
    A = np.column_stack([np.ones(n), x])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    s2 = resid @ resid / (n - 2)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
    assert res.beta == pytest.approx(beta)
    assert res.se == pytest.approx(se)
    assert res.r2 == pytest.approx(1 - resid @ resid / np.sum((y - y.mean()) ** 2))


def test_ols_without_intercept(rng):
    X = rng.normal(size=(100, 1))
    y = 3.0 * X[:, 0] + rng.normal(scale=1e-3, size=100)
    res = st.ols(X, y, add_intercept=False)
    assert res.beta.shape == (1,)
    assert res.beta[0] == pytest.approx(3.0, abs=1e-3)


def test_newey_west_zero_lags_is_white(rng):
    n = 300
    X = np.column_stack([np.ones(n), rng.normal(size=n)])
    u = rng.normal(size=n) * (1 + np.abs(X[:, 1]))
    Q_inv = np.linalg.inv(X.T @ X)
    white = np.sqrt(np.diag(Q_inv @ (X.T * u**2) @ X @ Q_inv))
    assert st.newey_west_se(X, u, lags=0) == pytest.approx(white)


def test_newey_west_larger_with_positive_autocorrelation(rng):
    n = 2000
    e = rng.normal(size=n)
    u = np.empty(n)
    u[0] = e[0]
    for t in range(1, n):
        u[t] = 0.8 * u[t - 1] + e[t]
    x = np.empty(n)
    x[0] = rng.normal()
    eta = rng.normal(size=n)
    for t in range(1, n):
        x[t] = 0.8 * x[t - 1] + eta[t]
    X = np.column_stack([np.ones(n), x])
    se0 = st.newey_west_se(X, u, lags=0)
    se10 = st.newey_west_se(X, u, lags=10)
    assert se10[1] > 1.5 * se0[1]


def test_bootstrap_ci_mean(rng):
    x = rng.normal(5.0, 1.0, size=400)
    lo, hi = st.bootstrap_ci(x, np.mean, 2000, 0.95, rng)
    se = x.std(ddof=1) / math.sqrt(len(x))
    assert lo < x.mean() < hi
    assert (hi - lo) == pytest.approx(2 * 1.96 * se, rel=0.15)


def test_permutation_test(rng):
    a = rng.normal(0.0, 1.0, size=100)
    b = rng.normal(1.0, 1.0, size=100)
    assert st.permutation_test(a, b, 2000, rng) < 0.01
    c = rng.normal(0.0, 1.0, size=100)
    d = rng.normal(0.0, 1.0, size=100)
    p = st.permutation_test(c, d, 2000, rng)
    assert 0.0 < p <= 1.0
    assert p >= 1 / 2001


def test_sharpe(rng):
    r = rng.normal(0.0005, 0.01, size=252 * 4)
    assert st.sharpe_ratio(r, 252) == pytest.approx(r.mean() / r.std(ddof=1) * math.sqrt(252))
    sr = r.mean() / r.std(ddof=1)
    assert st.sharpe_se(r) == pytest.approx(math.sqrt((1 + sr**2 / 2) / len(r)))

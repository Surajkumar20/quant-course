import numpy as np
import pytest
from scipy import optimize, stats

import portfolio as pf


@pytest.fixture
def rng():
    return np.random.default_rng(3)


@pytest.fixture
def cov(rng):
    A = rng.normal(size=(6, 6))
    return A @ A.T / 6 * 0.04 + np.diag(rng.uniform(0.01, 0.03, 6))


def test_min_variance(cov):
    w = pf.min_variance_weights(cov)
    assert w.sum() == pytest.approx(1.0)
    # no feasible perturbation lowers variance: gradient is parallel to 1
    g = cov @ w
    assert np.allclose(g, g.mean())
    # beats a numerical optimiser
    res = optimize.minimize(lambda v: v @ cov @ v, np.ones(6) / 6,
                            constraints={"type": "eq", "fun": lambda v: v.sum() - 1})
    assert w @ cov @ w <= res.fun + 1e-10


def test_two_asset_min_variance_closed_form():
    s1, s2, rho = 0.2, 0.3, 0.25
    cov = np.array([[s1**2, rho * s1 * s2], [rho * s1 * s2, s2**2]])
    w = pf.min_variance_weights(cov)
    w1 = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    assert w == pytest.approx([w1, 1 - w1])


def test_mean_variance(cov, rng):
    mu = rng.normal(0.05, 0.02, 6)
    w = pf.mean_variance_weights(mu, cov, risk_aversion=4.0)
    assert mu - 4.0 * cov @ w == pytest.approx(np.zeros(6), abs=1e-10)  # FOC


def test_tangency_maximises_sharpe(cov, rng):
    mu = rng.normal(0.06, 0.02, 6)
    w = pf.tangency_weights(mu, cov, rf=0.01)
    assert w.sum() == pytest.approx(1.0)
    sharpe = lambda v: (v @ mu - 0.01) / np.sqrt(v @ cov @ v)
    for _ in range(200):
        v = w + rng.normal(scale=0.05, size=6)
        v /= v.sum()
        assert sharpe(v) <= sharpe(w) + 1e-12


def test_ledoit_wolf_structure(rng):
    X = rng.normal(size=(40, 30))
    shrunk, delta = pf.ledoit_wolf(X)
    assert 0 <= delta <= 1
    Xc = X - X.mean(axis=0)
    S = Xc.T @ Xc / 40
    m = np.trace(S) / 30
    assert shrunk == pytest.approx(delta * m * np.eye(30) + (1 - delta) * S)
    assert np.linalg.cond(shrunk) < np.linalg.cond(S)
    assert delta > 0.3  # p close to T: heavy shrinkage


def test_ledoit_wolf_little_shrinkage_with_lots_of_data(rng):
    C = np.diag(np.linspace(0.5, 3.0, 5))
    X = rng.multivariate_normal(np.zeros(5), C, size=20_000)
    _, delta = pf.ledoit_wolf(X)
    assert delta < 0.05


def test_pca(rng):
    n, p = 5000, 8
    f = rng.normal(size=(n, 1))
    load = np.linspace(1, 2, p)
    X = f * load + 0.3 * rng.normal(size=(n, p))
    L, evr = pf.pca(X, 3)
    assert L.shape == (8, 3)
    assert L.T @ L == pytest.approx(np.eye(3), abs=1e-10)
    assert evr[0] > 0.8 and evr[0] > evr[1] >= evr[2]
    u = load / np.linalg.norm(load)
    assert abs(L[:, 0] @ u) == pytest.approx(1.0, abs=1e-3)


def test_risk_contributions_sum_to_vol(cov):
    w = np.array([0.3, 0.1, 0.2, -0.1, 0.25, 0.25])
    rc = pf.risk_contributions(w, cov)
    assert rc.sum() == pytest.approx(np.sqrt(w @ cov @ w))


def test_risk_parity(cov):
    w = pf.risk_parity_weights(cov)
    assert w.sum() == pytest.approx(1.0)
    assert np.all(w > 0)
    rc = pf.risk_contributions(w, cov)
    assert rc == pytest.approx(np.full(6, rc.mean()), rel=1e-6)


def test_risk_parity_diagonal_is_inverse_vol():
    vols = np.array([0.1, 0.2, 0.4])
    w = pf.risk_parity_weights(np.diag(vols**2))
    inv = 1 / vols
    assert w == pytest.approx(inv / inv.sum(), rel=1e-6)


def test_var_es(rng):
    pnl = rng.standard_t(4, size=100_000)
    var = pf.historical_var(pnl, 0.99)
    es = pf.historical_es(pnl, 0.99)
    assert var == pytest.approx(-np.quantile(pnl, 0.01))
    assert es == pytest.approx(-pnl[pnl <= -var].mean())
    assert es > var > 0
    assert pf.parametric_var(0.0, 1.0, 0.99) == pytest.approx(-stats.norm.ppf(0.01))
    assert pf.parametric_var(0.001, 0.02, 0.95) == pytest.approx(-(0.001 + 0.02 * stats.norm.ppf(0.05)))

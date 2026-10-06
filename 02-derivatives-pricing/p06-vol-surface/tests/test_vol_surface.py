import numpy as np
import pytest

import vol_surface as vs

# a well-behaved equity-like smile (T = 1): skewed, convex, arbitrage-free
GOOD = (0.02, 0.15, -0.6, 0.05, 0.2)
# Gatheral & Jacquier (2014) example of a smile with butterfly arbitrage, T = 1
BAD = (-0.0410, 0.1331, 0.3060, 0.3586, 0.4153)


def test_svi_total_variance_at_m():
    a, b, rho, m, s = GOOD
    w = vs.svi_total_variance(np.array([m]), GOOD)
    assert w[0] == pytest.approx(a + b * s)


def test_svi_wings_are_linear():
    a, b, rho, m, s = GOOD
    k = np.array([50.0, -50.0])
    w = vs.svi_total_variance(k, GOOD)
    assert (w[0] - vs.svi_total_variance(np.array([49.0]), GOOD)[0]) == pytest.approx(b * (1 + rho), rel=1e-3)
    assert (w[1] - vs.svi_total_variance(np.array([-49.0]), GOOD)[0]) == pytest.approx(b * (1 - rho), rel=1e-3)


def test_derivatives_match_finite_differences():
    k = np.linspace(-1.5, 1.5, 31)
    w, w1, w2 = vs.svi_derivatives(k, GOOD)
    h = 1e-5
    f = lambda x: vs.svi_total_variance(x, GOOD)
    assert w == pytest.approx(f(k))
    assert w1 == pytest.approx((f(k + h) - f(k - h)) / (2 * h), rel=1e-6, abs=1e-9)
    assert w2 == pytest.approx((f(k + 1e-3) - 2 * f(k) + f(k - 1e-3)) / 1e-6, rel=1e-4, abs=1e-6)


def test_butterfly_detection():
    assert not vs.has_butterfly_arbitrage(GOOD)
    assert vs.has_butterfly_arbitrage(BAD)
    g = vs.butterfly_g(np.linspace(-1.5, 1.5, 301), BAD)
    assert g.min() < 0


def test_density_integrates_to_one():
    k = np.linspace(-6, 6, 20001)
    p = vs.svi_density(k, GOOD)
    assert np.all(p >= 0)
    assert np.trapezoid(p, k) == pytest.approx(1.0, abs=2e-3)


def test_density_negative_when_arbitrage():
    k = np.linspace(-1.5, 1.5, 3001)
    assert vs.svi_density(k, BAD).min() < 0


def test_calendar_arbitrage():
    a, b, rho, m, s = GOOD
    short = (0.5, (a / 2, b / 2, rho, m, s))
    long_ = (1.0, GOOD)
    assert not vs.has_calendar_arbitrage([short, long_])
    assert vs.has_calendar_arbitrage([(0.5, GOOD), (1.0, (a / 2, b / 2, rho, m, s))])
    # crossing smiles: more variance at the wings for the short expiry
    crossing = (0.5, (0.0, 0.3, rho, m, s))
    assert vs.has_calendar_arbitrage([crossing, long_])


def test_fit_recovers_noiseless_smile():
    k = np.linspace(-0.8, 0.5, 40)
    w = vs.svi_total_variance(k, GOOD)
    fitted = vs.fit_svi(k, w)
    assert vs.svi_total_variance(k, fitted) == pytest.approx(w, abs=1e-6)


def test_fit_noisy_smile_is_close_in_vol_terms():
    rng = np.random.default_rng(0)
    k = np.linspace(-0.8, 0.5, 60)
    true_vol = np.sqrt(vs.svi_total_variance(k, GOOD))
    noisy = (true_vol + rng.normal(0, 0.002, size=k.shape)) ** 2
    fitted = vs.fit_svi(k, noisy)
    err = np.sqrt(vs.svi_total_variance(k, fitted)) - true_vol
    assert np.max(np.abs(err)) < 0.003  # within 0.3 vol points everywhere
    a, b, rho, m, s = fitted
    assert b >= 0 and abs(rho) < 1 and s > 0

import math

import pytest

from pricing import bs_greeks, bs_price, crr_price, implied_vol

BASE = dict(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.2)


# ---- Black-Scholes ---------------------------------------------------------

def test_bs_textbook_values():
    assert bs_price(**BASE, kind="call") == pytest.approx(10.450583572, abs=1e-6)
    assert bs_price(**BASE, kind="put") == pytest.approx(5.573526022, abs=1e-6)


def test_bs_with_dividends():
    # Hull-style example: S=K=100, T=0.5, r=10%, q=3%, sigma=25%
    c = bs_price(100, 100, 0.5, 0.10, 0.25, q=0.03, kind="call")
    p = bs_price(100, 100, 0.5, 0.10, 0.25, q=0.03, kind="put")
    assert c - p == pytest.approx(100 * math.exp(-0.015) - 100 * math.exp(-0.05), abs=1e-9)


@pytest.mark.parametrize("K", [60, 90, 100, 110, 150])
@pytest.mark.parametrize("T", [0.01, 0.5, 3.0])
def test_put_call_parity(K, T):
    S, r, sigma, q = 100, 0.03, 0.35, 0.01
    c = bs_price(S, K, T, r, sigma, q, "call")
    p = bs_price(S, K, T, r, sigma, q, "put")
    assert c - p == pytest.approx(S * math.exp(-q * T) - K * math.exp(-r * T), abs=1e-9)


def test_bs_limits():
    # deep ITM call ~ forward intrinsic, deep OTM ~ 0
    assert bs_price(100, 1, 1, 0.05, 0.2) == pytest.approx(100 - math.exp(-0.05), abs=1e-6)
    assert bs_price(100, 1000, 1, 0.05, 0.2) == pytest.approx(0.0, abs=1e-10)


# ---- Greeks ------------------------------------------------------------------

@pytest.mark.parametrize("kind", ["call", "put"])
@pytest.mark.parametrize("K", [80, 100, 125])
def test_greeks_match_finite_differences(kind, K):
    S, T, r, sigma, q = 100.0, 0.75, 0.04, 0.3, 0.02
    g = bs_greeks(S, K, T, r, sigma, q, kind)
    f = lambda **kw: bs_price(**{**dict(S=S, K=K, T=T, r=r, sigma=sigma, q=q, kind=kind), **kw})
    h = 1e-4
    assert g["delta"] == pytest.approx((f(S=S + h) - f(S=S - h)) / (2 * h), rel=1e-5)
    assert g["gamma"] == pytest.approx((f(S=S + 1e-2) - 2 * f() + f(S=S - 1e-2)) / 1e-4, rel=1e-3)
    assert g["vega"] == pytest.approx((f(sigma=sigma + h) - f(sigma=sigma - h)) / (2 * h), rel=1e-5)
    assert g["rho"] == pytest.approx((f(r=r + h) - f(r=r - h)) / (2 * h), rel=1e-5)
    assert g["theta"] == pytest.approx(-(f(T=T + h) - f(T=T - h)) / (2 * h), rel=1e-5)


def test_call_put_gamma_vega_equal():
    c = bs_greeks(**BASE, kind="call")
    p = bs_greeks(**BASE, kind="put")
    assert c["gamma"] == pytest.approx(p["gamma"])
    assert c["vega"] == pytest.approx(p["vega"])
    assert c["delta"] - p["delta"] == pytest.approx(1.0)


# ---- implied vol ---------------------------------------------------------------

@pytest.mark.parametrize("kind", ["call", "put"])
@pytest.mark.parametrize("K", [50, 80, 100, 120, 200])
@pytest.mark.parametrize("sigma", [0.05, 0.2, 0.8])
def test_implied_vol_roundtrip(kind, K, sigma):
    S, T, r = 100, 0.5, 0.02
    price = bs_price(S, K, T, r, sigma, 0.0, kind)
    if bs_greeks(S, K, T, r, sigma, 0.0, kind)["vega"] < 1e-3:
        pytest.skip("vega ~ 0: price carries no information about vol (why? explain in your write-up)")
    assert implied_vol(price, S, K, T, r, 0.0, kind) == pytest.approx(sigma, abs=1e-6)


def test_implied_vol_rejects_arbitrage():
    with pytest.raises(ValueError):
        implied_vol(120.0, 100, 100, 1, 0.0)        # call worth more than the stock
    with pytest.raises(ValueError):
        implied_vol(1.0, 100, 50, 1, 0.0)           # call below intrinsic


# ---- binomial tree -------------------------------------------------------------

def test_crr_converges_to_bs():
    for kind in ("call", "put"):
        bs = bs_price(**BASE, kind=kind)
        assert crr_price(**BASE, steps=2000, kind=kind) == pytest.approx(bs, abs=5e-3)


def test_crr_one_step_by_hand():
    # one step: u = e^{0.2}, d = e^{-0.2}, p = (e^{0.05} - d)/(u - d)
    u, d = math.exp(0.2), math.exp(-0.2)
    p = (math.exp(0.05) - d) / (u - d)
    expected = math.exp(-0.05) * p * (100 * u - 100)
    assert crr_price(**BASE, steps=1) == pytest.approx(expected)


def test_american_put_premium():
    euro = crr_price(**BASE, steps=1000, kind="put")
    amer = crr_price(**BASE, steps=1000, kind="put", american=True)
    assert amer > euro + 0.4
    assert amer == pytest.approx(6.0896, abs=5e-3)


def test_american_call_no_dividend_equals_european():
    euro = crr_price(**BASE, steps=500, kind="call")
    amer = crr_price(**BASE, steps=500, kind="call", american=True)
    assert amer == pytest.approx(euro, abs=1e-10)


def test_american_call_with_dividend_has_premium():
    euro = crr_price(**BASE, steps=500, q=0.08, kind="call")
    amer = crr_price(**BASE, steps=500, q=0.08, kind="call", american=True)
    assert amer > euro

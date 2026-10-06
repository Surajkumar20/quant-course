import math

import numpy as np
import pytest

import mm

GAMMA, SIGMA, K, A, T = 0.1, 2.0, 1.5, 140.0, 1.0


def test_reservation_price():
    assert mm.reservation_price(100, 0, GAMMA, SIGMA, 0.5) == pytest.approx(100)
    assert mm.reservation_price(100, 3, GAMMA, SIGMA, 0.5) == pytest.approx(100 - 3 * 0.1 * 4 * 0.5)
    assert mm.reservation_price(100, -2, GAMMA, SIGMA, 0.5) > 100


def test_optimal_spread():
    expected = 0.1 * 4 * 0.5 + (2 / 0.1) * math.log(1 + 0.1 / 1.5)
    assert mm.optimal_spread(GAMMA, SIGMA, 0.5, K) == pytest.approx(expected)
    # shrinks as the horizon approaches; never below the tau=0 floor
    assert mm.optimal_spread(GAMMA, SIGMA, 0.0, K) < mm.optimal_spread(GAMMA, SIGMA, 1.0, K)
    # gamma -> 0 limit is 2/k
    assert mm.optimal_spread(1e-8, SIGMA, 1.0, K) == pytest.approx(2 / K, rel=1e-6)


def test_as_quotes():
    bid, ask = mm.as_quotes(100, 2, GAMMA, SIGMA, 0.5, K)
    r = mm.reservation_price(100, 2, GAMMA, SIGMA, 0.5)
    sp = mm.optimal_spread(GAMMA, SIGMA, 0.5, K)
    assert (bid, ask) == pytest.approx((r - sp / 2, r + sp / 2))
    assert bid < ask


def test_fill_probability():
    dt = 0.005
    p = mm.fill_probability(np.array([0.0, 0.5, 1.0, 3.0]), A, K, dt)
    assert p[0] == pytest.approx(1 - math.exp(-A * dt))
    assert np.all(np.diff(p) < 0)
    assert mm.fill_probability(1.0, 0.0, K, dt) == pytest.approx(0.0)


def test_simulate_no_flow_means_no_trades():
    res = mm.simulate(lambda t, s, q: (s - 1, s + 1), np.random.default_rng(0), A=0.0)
    assert res.pnl == pytest.approx(0.0)
    assert res.final_q == 0 and res.n_bid_fills == 0 and res.n_ask_fills == 0
    assert res.q_path.shape == (200,)


def test_simulate_accounting_consistency():
    rng = np.random.default_rng(1)
    res = mm.simulate(lambda t, s, q: (s - 0.5, s + 0.5), rng)
    assert res.final_q == res.n_bid_fills - res.n_ask_fills
    assert res.q_path[-1] == res.final_q
    assert np.all(np.abs(np.diff(res.q_path)) <= 2)


def test_inventory_strategy_reduces_risk():
    """The core result of the paper: same spread, but skewing by inventory cuts P&L dispersion."""
    rng = np.random.default_rng(42)
    dt = T / 200

    def inventory(t, s, q):
        return mm.as_quotes(s, q, GAMMA, SIGMA, T - t, K)

    def symmetric(t, s, q):
        half = mm.optimal_spread(GAMMA, SIGMA, T - t, K) / 2
        return s - half, s + half

    inv = [mm.simulate(inventory, rng) for _ in range(300)]
    sym = [mm.simulate(symmetric, rng) for _ in range(300)]
    inv_pnl = np.array([r.pnl for r in inv])
    sym_pnl = np.array([r.pnl for r in sym])
    assert inv_pnl.std() < 0.7 * sym_pnl.std()
    assert np.mean([abs(r.final_q) for r in inv]) < 0.6 * np.mean([abs(r.final_q) for r in sym])
    assert inv_pnl.mean() > 0  # still profitable on average

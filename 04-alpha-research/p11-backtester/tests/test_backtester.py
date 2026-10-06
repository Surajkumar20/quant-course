import math

import numpy as np
import pandas as pd
import pytest

from backtester import max_drawdown, performance_stats, run_backtest


def make_prices(**cols):
    n = len(next(iter(cols.values())))
    return pd.DataFrame(cols, index=pd.bdate_range("2024-01-01", periods=n), dtype=float)


class Fixed:
    """Emits a given target dict at specific bars."""

    def __init__(self, schedule):
        self.schedule = schedule

    def on_bar(self, t, history):
        return self.schedule.get(t, {})


def test_buy_and_hold_exact_accounting():
    px = make_prices(A=[10, 11, 12, 9, 15])
    res = run_backtest(px, Fixed({0: {"A": 100}}), initial_cash=10_000, cost_bps=0)
    # decided at bar 0, filled at close of bar 1 (price 11)
    assert list(res.positions["A"]) == [0, 100, 100, 100, 100]
    expected = [10_000, 10_000, 10_000 + 100, 10_000 - 200, 10_000 + 400]
    assert list(res.equity) == pytest.approx(expected)
    assert len(res.fills) == 1
    f = res.fills[0]
    assert (f.date, f.symbol, f.qty, f.price) == (px.index[1], "A", 100, 11)


def test_targets_on_last_bar_are_not_filled():
    px = make_prices(A=[10, 11, 12])
    res = run_backtest(px, Fixed({2: {"A": 50}}), initial_cash=1000)
    assert res.fills == []
    assert list(res.equity) == pytest.approx([1000, 1000, 1000])


def test_strategy_never_sees_the_future():
    px = make_prices(A=np.arange(1, 31), B=np.arange(101, 131))
    seen = []

    class Spy:
        def on_bar(self, t, history):
            seen.append((t, len(history), history.index[-1]))
            return {}

    run_backtest(px, Spy())
    assert [s[0] for s in seen] == list(range(30))
    for t, n, last in seen:
        assert n == t + 1
        assert last == px.index[t]


def test_transaction_costs_round_trip():
    px = make_prices(A=[100, 100, 100, 100])
    res = run_backtest(px, Fixed({0: {"A": 10}, 1: {"A": 0}}), initial_cash=10_000, cost_bps=10)
    # buy 10 @100 at bar 1, sell 10 @100 at bar 2; 10 bps on 1000 notional each way = 1.0 + 1.0
    assert res.total_cost == pytest.approx(2.0)
    assert res.equity.iloc[-1] == pytest.approx(10_000 - 2.0)
    assert [f.cost for f in res.fills] == pytest.approx([1.0, 1.0])


def test_short_selling():
    px = make_prices(A=[50, 50, 40, 60])
    res = run_backtest(px, Fixed({0: {"A": -10}}), initial_cash=1000)
    assert list(res.equity) == pytest.approx([1000, 1000, 1100, 900])


def test_unchanged_target_does_not_trade():
    px = make_prices(A=[10, 11, 12, 13, 14])

    class Hold:
        def on_bar(self, t, history):
            return {"A": 5}

    res = run_backtest(px, Hold(), cost_bps=5)
    assert len(res.fills) == 1


def test_omitted_symbols_keep_positions_multi_asset():
    px = make_prices(A=[10, 10, 10, 20], B=[5, 5, 6, 6])
    res = run_backtest(px, Fixed({0: {"A": 1, "B": 2}, 1: {"B": 0}}), initial_cash=100)
    assert list(res.positions["A"]) == [0, 1, 1, 1]
    assert list(res.positions["B"]) == [0, 2, 0, 0]
    # bar 2: sold B at 6 -> +2 gain; bar 3: A doubles -> +10
    assert list(res.equity) == pytest.approx([100, 100, 102, 112])


def test_max_drawdown():
    eq = pd.Series([100, 120, 90, 130, 65, 70], dtype=float)
    assert max_drawdown(eq) == pytest.approx(-0.5)
    assert max_drawdown(pd.Series([1.0, 2.0, 3.0])) == pytest.approx(0.0)


def test_performance_stats():
    rng = np.random.default_rng(1)
    r = rng.normal(0.0005, 0.01, 1000)
    eq = pd.Series(1e6 * np.cumprod(np.concatenate([[1.0], 1 + r])))
    s = performance_stats(eq)
    assert s["sharpe"] == pytest.approx(r.mean() / r.std(ddof=1) * math.sqrt(252))
    assert s["ann_vol"] == pytest.approx(r.std(ddof=1) * math.sqrt(252))
    assert s["cagr"] == pytest.approx((eq.iloc[-1] / eq.iloc[0]) ** (252 / 1000) - 1)
    assert s["max_drawdown"] == pytest.approx(max_drawdown(eq))
    assert s["calmar"] == pytest.approx(s["cagr"] / abs(s["max_drawdown"]))
    assert s["hit_rate"] == pytest.approx((r > 0).mean())

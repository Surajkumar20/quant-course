"""Event-driven daily backtester. See README.md for the execution model the tests enforce."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

import pandas as pd


class Strategy(Protocol):
    def on_bar(self, t: int, history: pd.DataFrame) -> dict[str, float]:
        """Called at bar t with history = prices.iloc[:t+1].

        Return target positions in shares, {symbol: shares}. Symbols omitted keep their current
        position. Returning {} means "no change".
        """
        ...


@dataclass
class Fill:
    date: pd.Timestamp
    symbol: str
    qty: float          # signed shares traded
    price: float
    cost: float         # transaction cost paid in cash (>= 0)


@dataclass
class BacktestResult:
    equity: pd.Series              # indexed like prices; equity after fills at each close
    positions: pd.DataFrame        # dates x symbols, shares held after fills at each close
    fills: list[Fill] = field(default_factory=list)
    total_cost: float = 0.0


def run_backtest(
    prices: pd.DataFrame,
    strategy: Strategy,
    initial_cash: float = 1_000_000.0,
    cost_bps: float = 0.0,
) -> BacktestResult:
    raise NotImplementedError


def max_drawdown(equity: pd.Series) -> float:
    """Most negative peak-to-trough return, e.g. -0.25 for a 25% drawdown (0.0 if none)."""
    raise NotImplementedError


def performance_stats(equity: pd.Series, periods_per_year: int = 252) -> dict[str, float]:
    """Return {"cagr", "ann_vol", "sharpe", "max_drawdown", "calmar", "hit_rate"}.

    Use simple daily returns of `equity`; sharpe = mean/std(ddof=1)*sqrt(periods_per_year) with
    zero risk-free rate; cagr from first to last equity with years = (len(equity)-1)/periods_per_year;
    calmar = cagr / |max_drawdown|; hit_rate = fraction of days with return > 0.
    """
    raise NotImplementedError

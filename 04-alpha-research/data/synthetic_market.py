#!/usr/bin/env python3
"""Synthetic daily equity market with known ground truth.

    from synthetic_market import make_market
    mkt = make_market(n_assets=50, n_days=2520, seed=0)
    mkt.prices          # DataFrame (dates x tickers), close prices
    mkt.returns         # simple daily returns
    mkt.pairs           # list of (ticker_y, ticker_x, beta) cointegrated pairs
    mkt.signal          # DataFrame: a feature that predicts next-day returns with IC ~ signal_ic

Or from the command line: python synthetic_market.py --out prices.csv

Structure:
  * 3 latent factors (market, plus two style factors) with fat-tailed (t, 5 dof) shocks
  * GARCH(1,1)-style volatility clustering in the market factor
  * idiosyncratic noise
  * a few cointegrated pairs: y = beta * x + OU spread
  * a planted predictive signal: noisy view of tomorrow's idiosyncratic return

Don't look at how `signal` is constructed until after p14. Treat it as an unknown alpha.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Market:
    prices: pd.DataFrame
    returns: pd.DataFrame
    pairs: list[tuple[str, str, float]]
    signal: pd.DataFrame
    factor_returns: pd.DataFrame


def make_market(
    n_assets: int = 50,
    n_days: int = 2520,
    n_pairs: int = 3,
    signal_ic: float = 0.03,
    seed: int = 0,
) -> Market:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2015-01-02", periods=n_days)
    tickers = [f"S{i:03d}" for i in range(n_assets)]

    # --- factors -------------------------------------------------------------
    t5 = lambda size: rng.standard_t(5, size=size) / np.sqrt(5 / 3)  # unit-variance t(5)
    mkt = np.empty(n_days)
    var = 0.01**2
    omega, alpha, beta = 0.01**2 * 0.05, 0.08, 0.87
    for t in range(n_days):
        mkt[t] = 0.0003 + np.sqrt(var) * t5(1)[0]
        var = omega + alpha * (mkt[t] - 0.0003) ** 2 + beta * var
    style = t5((n_days, 2)) * np.array([0.005, 0.004])
    factors = np.column_stack([mkt, style])

    loadings = np.column_stack(
        [rng.normal(1.0, 0.3, n_assets), rng.normal(0, 1, n_assets), rng.normal(0, 1, n_assets)]
    )
    idio_vol = rng.uniform(0.008, 0.025, n_assets)
    idio = t5((n_days, n_assets)) * idio_vol

    # --- planted signal: noisy view of tomorrow's idiosyncratic return ---------
    z_next = np.vstack([idio[1:] / idio_vol, np.zeros((1, n_assets))])
    noise = rng.normal(size=(n_days, n_assets))
    signal = signal_ic * z_next + np.sqrt(1 - signal_ic**2) * noise
    signal[-1] = noise[-1]

    rets = factors @ loadings.T + idio

    # --- cointegrated pairs: overwrite some assets' log-prices -----------------
    logp = np.log(50) + np.cumsum(np.log1p(np.clip(rets, -0.5, None)), axis=0)
    pairs = []
    for k in range(n_pairs):
        iy, ix = n_assets - 1 - 2 * k, n_assets - 2 - 2 * k
        b = float(rng.uniform(0.6, 1.4))
        kappa, sigma_s = rng.uniform(0.03, 0.1), 0.01
        s = np.empty(n_days)
        s[0] = 0.0
        for t in range(1, n_days):
            s[t] = s[t - 1] * (1 - kappa) + sigma_s * rng.normal()
        logp[:, iy] = 0.5 + b * logp[:, ix] + s
        pairs.append((tickers[iy], tickers[ix], b))

    prices = pd.DataFrame(np.exp(logp), index=dates, columns=tickers)
    returns = prices.pct_change().iloc[1:]
    return Market(
        prices=prices,
        returns=returns,
        pairs=pairs,
        signal=pd.DataFrame(signal, index=dates, columns=tickers),
        factor_returns=pd.DataFrame(factors, index=dates, columns=["mkt", "style1", "style2"]),
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="prices.csv")
    ap.add_argument("--assets", type=int, default=50)
    ap.add_argument("--days", type=int, default=2520)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    m = make_market(a.assets, a.days, seed=a.seed)
    m.prices.to_csv(a.out)
    print(f"wrote {m.prices.shape} prices to {a.out}")

#!/usr/bin/env python3
"""Generate a synthetic, arbitrage-free option chain with bid/ask noise.

    python 02-derivatives-pricing/p06-vol-surface/data/generate_chain.py --out chain.csv

The true surface is SSVI (Gatheral & Jacquier 2014), which is free of static arbitrage for the
parameters used here. Your job is to recover it from noisy quotes. Don't read `true_surface`
until you have fitted your own surface.

Columns: expiry (years), strike, forward, rate, call_bid, call_ask, put_bid, put_ask
"""
from __future__ import annotations

import argparse
import csv
import math

import numpy as np
from scipy.stats import norm

SPOT = 4500.0
RATE = 0.04
DIV = 0.015
EXPIRIES = [0.08, 0.25, 0.5, 1.0, 1.5, 2.0]


def true_surface(k: np.ndarray, T: float) -> np.ndarray:
    """SSVI total variance with a power-law phi. theta(T) is ATM total variance."""
    theta = 0.04 * T + 0.002 * (1 - math.exp(-3 * T))
    rho, eta, gamma = -0.65, 1.1, 0.4
    phi = eta / (theta**gamma * (1 + theta) ** (1 - gamma))
    return 0.5 * theta * (1 + rho * phi * k + np.sqrt((phi * k + rho) ** 2 + 1 - rho**2))


def bs(F: float, K: np.ndarray, T: float, r: float, vol: np.ndarray, call: bool) -> np.ndarray:
    v = vol * math.sqrt(T)
    d1 = (np.log(F / K) + 0.5 * v * v) / v
    d2 = d1 - v
    df = math.exp(-r * T)
    if call:
        return df * (F * norm.cdf(d1) - K * norm.cdf(d2))
    return df * (K * norm.cdf(-d2) - F * norm.cdf(-d1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="chain.csv")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    rows = []
    for T in EXPIRIES:
        F = SPOT * math.exp((RATE - DIV) * T)
        width = 3.5 * 0.2 * math.sqrt(T)
        strikes = np.round(F * np.exp(np.linspace(-width, 0.6 * width, 41)) / 5) * 5
        strikes = np.unique(strikes)
        k = np.log(strikes / F)
        vol = np.sqrt(true_surface(k, T) / T)
        for call in (True, False):
            mid = bs(F, strikes, T, RATE, vol, call)
            # spreads: wider for cheap options and short expiries, plus mid noise
            spread = np.maximum(0.05, 0.02 * mid) * (1 + 0.5 / math.sqrt(T))
            noisy_mid = mid * (1 + rng.normal(0, 0.003, size=mid.shape))
            bid = np.maximum(np.round((noisy_mid - spread / 2) / 0.05) * 0.05, 0.0)
            ask = np.round((noisy_mid + spread / 2) / 0.05) * 0.05 + 0.05
            if call:
                cb, ca = bid, ask
            else:
                pb, pa = bid, ask
        for i, K in enumerate(strikes):
            rows.append([T, K, round(F, 4), RATE, cb[i], ca[i], pb[i], pa[i]])

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["expiry", "strike", "forward", "rate", "call_bid", "call_ask", "put_bid", "put_ask"])
        for r in rows:
            w.writerow([f"{x:.6g}" if isinstance(x, float) else x for x in r])
    print(f"wrote {len(rows)} strikes x 2 to {args.out}")


if __name__ == "__main__":
    main()

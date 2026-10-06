"""European/American vanilla option pricing.

Conventions (the tests rely on these):
  * S spot, K strike, T years to expiry, r continuously-compounded rate,
    sigma annualised vol, q continuous dividend yield, kind in {"call", "put"}.
  * delta = dV/dS, gamma = d2V/dS2
  * vega  = dV/dsigma        (per 1.00 of vol, NOT per 1%)
  * theta = dV/dt            (per year, calendar time passing; i.e. -dV/dT; usually negative)
  * rho   = dV/dr            (per 1.00 of rate)
You may use scipy.stats.norm for the normal CDF/PDF.
"""
from __future__ import annotations


def bs_price(S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0, kind: str = "call") -> float:
    raise NotImplementedError


def bs_greeks(
    S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0, kind: str = "call"
) -> dict[str, float]:
    """Return {"delta", "gamma", "vega", "theta", "rho"}."""
    raise NotImplementedError


def implied_vol(
    price: float, S: float, K: float, T: float, r: float, q: float = 0.0, kind: str = "call", tol: float = 1e-10
) -> float:
    """Black-Scholes implied volatility.

    Raise ValueError if `price` violates the no-arbitrage bounds
    (call: max(S e^{-qT} - K e^{-rT}, 0) < price < S e^{-qT}; put analogous).
    """
    raise NotImplementedError


def crr_price(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    steps: int,
    q: float = 0.0,
    kind: str = "call",
    american: bool = False,
) -> float:
    """Cox-Ross-Rubinstein binomial tree: u = exp(sigma sqrt(dt)), d = 1/u."""
    raise NotImplementedError

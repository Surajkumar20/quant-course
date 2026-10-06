"""Avellaneda-Stoikov market making."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

Strategy = Callable[[float, float, int], tuple[float, float]]  # (t, mid, inventory) -> (bid, ask)


def reservation_price(s: float, q: int, gamma: float, sigma: float, tau: float) -> float:
    """r = s - q * gamma * sigma^2 * tau   (tau = T - t)."""
    raise NotImplementedError


def optimal_spread(gamma: float, sigma: float, tau: float, k: float) -> float:
    """Total spread: gamma sigma^2 tau + (2/gamma) ln(1 + gamma/k)."""
    raise NotImplementedError


def as_quotes(s: float, q: int, gamma: float, sigma: float, tau: float, k: float) -> tuple[float, float]:
    """(bid, ask) = reservation price -/+ half the optimal spread."""
    raise NotImplementedError


def fill_probability(delta: float | np.ndarray, A: float, k: float, dt: float) -> float | np.ndarray:
    """P(at least one fill in dt) = 1 - exp(-A exp(-k delta) dt)."""
    raise NotImplementedError


@dataclass
class SimResult:
    pnl: float                 # cash + q * mid at the end
    final_q: int
    n_bid_fills: int
    n_ask_fills: int
    q_path: np.ndarray         # inventory after each step, length n_steps


def simulate(
    strategy: Strategy,
    rng: np.random.Generator,
    T: float = 1.0,
    n_steps: int = 200,
    s0: float = 100.0,
    sigma: float = 2.0,
    A: float = 140.0,
    k: float = 1.5,
) -> SimResult:
    """One Avellaneda-Stoikov simulation path.

    For each step i = 0..n_steps-1 with t = i * dt:
      1. (bid, ask) = strategy(t, s, q)
      2. with prob fill_probability(s - bid) we buy 1 at bid; independently,
         with prob fill_probability(ask - s) we sell 1 at ask
      3. s += sigma * sqrt(dt) * (+1 or -1 with equal probability)
      4. record q
    """
    raise NotImplementedError

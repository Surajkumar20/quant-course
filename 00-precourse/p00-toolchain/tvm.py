"""Time value of money. Implement every function; don't change the signatures."""
from __future__ import annotations

from collections.abc import Sequence


def future_value(pv: float, rate: float, n: int) -> float:
    """Value of `pv` after `n` periods compounding at `rate` per period."""
    raise NotImplementedError


def present_value(fv: float, rate: float, n: int) -> float:
    """Value today of `fv` received after `n` periods."""
    raise NotImplementedError


def npv(rate: float, cashflows: Sequence[float]) -> float:
    """Net present value; cashflows[0] occurs today (t = 0)."""
    raise NotImplementedError


def irr(cashflows: Sequence[float], tol: float = 1e-10) -> float:
    """Internal rate of return by bisection on [-0.99, 10].

    Raise ValueError if npv does not change sign on that interval.
    """
    raise NotImplementedError

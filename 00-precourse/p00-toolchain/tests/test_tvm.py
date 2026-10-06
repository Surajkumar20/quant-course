import pytest

from tvm import future_value, irr, npv, present_value


def test_future_value():
    assert future_value(100, 0.05, 0) == pytest.approx(100)
    assert future_value(100, 0.05, 2) == pytest.approx(110.25)


def test_present_value_inverts_future_value():
    for r in (0.0, 0.01, 0.07, 0.25):
        for n in (1, 5, 30):
            assert present_value(future_value(123.0, r, n), r, n) == pytest.approx(123.0)


def test_npv_two_year_bond():
    assert npv(0.05, [0, 100, 100]) == pytest.approx(185.9410430839)


def test_npv_cashflow_at_t0_is_not_discounted():
    assert npv(0.5, [-42.0]) == pytest.approx(-42.0)


def test_irr_simple():
    # pay 100 today, get 110 next year -> 10%
    assert irr([-100, 110]) == pytest.approx(0.10, abs=1e-8)


def test_irr_annuity():
    cfs = [-1000] + [100] * 20
    r = irr(cfs)
    assert npv(r, cfs) == pytest.approx(0, abs=1e-6)
    assert r == pytest.approx(0.0775, abs=1e-4)


def test_irr_no_sign_change_raises():
    with pytest.raises(ValueError):
        irr([100, 100, 100])

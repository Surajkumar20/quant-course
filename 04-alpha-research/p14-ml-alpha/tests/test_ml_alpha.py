import numpy as np
import pytest
from scipy import stats

import ml_alpha as ml


def test_purged_kfold_small_example():
    splits = ml.purged_kfold_splits(n=20, n_splits=4, label_horizon=2, embargo=1)
    assert len(splits) == 4
    train, test = splits[1]  # test = 5..9; purge 3..11, embargo 12
    assert list(test) == [5, 6, 7, 8, 9]
    assert list(train) == [0, 1, 2, 13, 14, 15, 16, 17, 18, 19]
    train0, test0 = splits[0]  # test 0..4 -> remove up to 4+2+1 = 7
    assert list(train0) == list(range(8, 20))
    train3, test3 = splits[3]  # test 15..19 -> remove 13..
    assert list(train3) == list(range(0, 13))


@pytest.mark.parametrize("n,k,h,e", [(100, 5, 0, 0), (257, 6, 5, 3), (1000, 10, 20, 10)])
def test_purged_kfold_properties(n, k, h, e):
    splits = ml.purged_kfold_splits(n, k, h, e)
    all_test = np.concatenate([t for _, t in splits])
    assert sorted(all_test.tolist()) == list(range(n))  # each sample tested exactly once
    for train, test in splits:
        a, b = test.min(), test.max()
        assert len(np.intersect1d(train, test)) == 0
        # no train label window [i, i+h] overlaps any test label window [a, b+h]
        assert not np.any((train <= b + h) & (train + h >= a))
        # embargo respected
        assert not np.any((train > b) & (train <= b + h + e))
    if h == 0 and e == 0:
        assert all(len(tr) + len(te) == n for tr, te in splits)


def test_walk_forward():
    splits = ml.walk_forward_splits(n=100, train_size=50, test_size=10, gap=5)
    assert len(splits) == 4  # tests start at 55, 65, 75, 85
    train, test = splits[0]
    assert list(train) == list(range(0, 50))
    assert list(test) == list(range(55, 65))
    train, test = splits[-1]
    assert list(train) == list(range(30, 80))
    assert list(test) == list(range(85, 95))
    for tr, te in splits:
        assert tr.max() + 5 < te.min()


def test_rank_ic_matches_scipy():
    rng = np.random.default_rng(0)
    a = rng.normal(size=200)
    b = 0.3 * a + rng.normal(size=200)
    assert ml.rank_ic(a, b) == pytest.approx(stats.spearmanr(a, b).statistic)


def test_rank_ic_handles_ties_and_nans():
    a = np.array([1.0, 2.0, 2.0, 3.0, np.nan, 5.0])
    b = np.array([1.0, 3.0, 2.0, 4.0, 9.0, np.nan])
    mask = ~np.isnan(a) & ~np.isnan(b)
    assert ml.rank_ic(a, b) == pytest.approx(stats.spearmanr(a[mask], b[mask]).statistic)


def test_psr_known_values():
    assert ml.probabilistic_sharpe_ratio(0.0, 0.0, 100) == pytest.approx(0.5)
    # SR 0.1/day over 253 obs, normal returns
    assert ml.probabilistic_sharpe_ratio(0.1, 0.0, 253) == pytest.approx(0.94337, abs=1e-4)
    # more data -> more confidence
    assert ml.probabilistic_sharpe_ratio(0.05, 0.0, 1000) > ml.probabilistic_sharpe_ratio(0.05, 0.0, 100)
    # negative skew / fat tails -> less confidence
    assert ml.probabilistic_sharpe_ratio(0.1, 0.0, 253, skew=-1, kurt=8) < ml.probabilistic_sharpe_ratio(0.1, 0.0, 253)


def test_expected_max_sharpe():
    assert ml.expected_max_sharpe(1, 0.5) == 0.0
    v = [ml.expected_max_sharpe(n, 1.0) for n in (2, 10, 100, 1000)]
    assert all(x < y for x, y in zip(v, v[1:]))
    # compare with Monte Carlo max of 100 iid standard normals (E ~ 2.508)
    rng = np.random.default_rng(1)
    mc = rng.normal(size=(20_000, 100)).max(axis=1).mean()
    assert ml.expected_max_sharpe(100, 1.0) == pytest.approx(mc, rel=0.03)
    assert ml.expected_max_sharpe(100, 4.0) == pytest.approx(2 * ml.expected_max_sharpe(100, 1.0))


def test_deflated_sharpe():
    sr, T = 0.08, 1000
    assert ml.deflated_sharpe_ratio(sr, 1, 0.001, T) == pytest.approx(ml.probabilistic_sharpe_ratio(sr, 0.0, T))
    few = ml.deflated_sharpe_ratio(sr, 5, 0.001, T)
    many = ml.deflated_sharpe_ratio(sr, 500, 0.001, T)
    assert many < few < ml.probabilistic_sharpe_ratio(sr, 0.0, T)

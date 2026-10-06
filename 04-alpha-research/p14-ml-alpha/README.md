# p14: ML Alpha Without Fooling Yourself

**Time:** ~2 weeks · **Language:** Python · **Track weight:** QR ★★★ QT ★ QD ★

> Financial data is mostly noise, it isn't stationary, and its samples overlap in time.
> Standard ML practice (shuffle, k-fold, pick the best model) gives you a beautiful backtest and a strategy that loses money.
> This project is about the validation machinery, and the model is the easy part.

## Reading
- [6.036](https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/): regression, regularisation, validation, features, (optionally) neural nets.
- [18.650](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/): multiple hypothesis testing.
- López de Prado, *Advances in Financial ML*, ch. 7 (cross-validation in finance), ch. 8 (feature importance), ch. 14 (backtest statistics).
- Bailey & López de Prado, *The Deflated Sharpe Ratio* (2014), and Harvey, Liu & Zhu, *…and the Cross-Section of Expected Returns* (2016).

## What you'll build
[`ml_alpha.py`](ml_alpha.py):
- `purged_kfold_splits`: k-fold that **purges** training samples whose labels overlap the test period, plus an **embargo**
- `walk_forward_splits`: rolling train/test windows with a gap
- `rank_ic`: Spearman rank information coefficient for one cross-section
- `probabilistic_sharpe_ratio`, `expected_max_sharpe`, `deflated_sharpe_ratio`

## Milestones
1. Make the tests pass.
2. **Features:** on the synthetic market, build ≥ 10 features per asset per day: lagged returns at several horizons, volatility, z-scores, cross-sectional ranks, and the provided `mkt.signal`. Use **only** information available at the close of day t.
3. **Labels:** 5-day forward returns. That makes neighbouring samples overlap. Explain why that breaks plain k-fold.
4. **Leakage demo:** fit ridge regression (your own implementation from p03, or scikit-learn) with (a) shuffled k-fold, (b) purged k-fold and (c) walk-forward. Report the IC from each. (a) should look suspiciously good.
5. **Search and deflate:** try ≥ 20 model/feature variants (log them all in `RESEARCH_LOG.md`), and pick the best by validation Sharpe. Then compute its **Deflated Sharpe Ratio** using your number of trials. Does it survive?
6. Turn the final predictions into a portfolio with p13 and backtest it with p11, including costs. Report gross and net Sharpe, turnover and capacity thoughts.

## Explain it in an interview
- Why is shuffled k-fold invalid for overlapping financial labels? What do purging and embargo fix?
- You tried 200 strategies and the best has Sharpe 2.1. How do you decide if it's real?
- What is an IC of 0.02 worth? (Grinold's fundamental law: IR ≈ IC·√breadth.)
- Why do tree models often beat linear ones on returns data, and why do they also overfit more?
- How would you detect that your alpha has decayed in production?

## Stretch
- Gradient-boosted trees (LightGBM) with purged CV and early stopping.
- Feature importance via mean decrease in accuracy on purged CV, compared with the in-sample importance.
- Combinatorial purged CV (CPCV) to get a *distribution* of backtest Sharpe ratios.

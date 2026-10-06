# p03: Statistics Toolkit (from scratch)

**Time:** ~3 weeks · **Language:** Python (numpy; scipy only for distribution functions) · **Track weight:** QR ★★★ QT ★★ QD ★

> Most strategies that look profitable are noise. This project gives you the tools to tell the difference,
> and to explain *why* a t-stat of 2 on a backtest you tried 200 variations of means nothing.

## Reading
- [18.650 Statistics for Applications](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/): all of it. The core is parametric inference & MLE, hypothesis testing, linear regression and the bootstrap.
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) Lecture 6 (regression analysis).
- Andrew Lo, *The Statistics of Sharpe Ratios* (Financial Analysts Journal, 2002). Short and important.

## What you'll build
[`stats_toolkit.py`](stats_toolkit.py):

| Function | Notes |
|---|---|
| `mle_normal(x)` | closed-form MLE (note: σ̂ uses 1/n, not 1/(n−1)) |
| `mle_exponential(x)` | closed form |
| `mle_numeric(neg_log_lik, x0)` | generic MLE via `scipy.optimize.minimize`, returning the params **and** standard errors from the inverse Hessian |
| `one_sample_t_test(x, mu0)` | t-stat and two-sided p-value, computed by you (scipy only for the t CDF) |
| `ols(X, y)` | β, classical standard errors, t-stats, R², residuals. Do **not** call a regression library |
| `newey_west_se(X, resid, lags)` | HAC standard errors, because financial residuals are autocorrelated |
| `bootstrap_ci(x, stat, n_boot, level, rng)` | percentile bootstrap |
| `permutation_test(x, y, n_perm, rng)` | two-sided p-value for a difference in means |
| `sharpe_ratio(r, periods_per_year)` / `sharpe_se(r)` | annualised Sharpe and Lo's iid standard error of the per-period Sharpe |

## Milestones
1. MLEs and the t-test, checked against `scipy.stats` in your own extra tests.
2. `ols`, checked against `numpy.linalg.lstsq` and (in a notebook) `statsmodels`.
3. Bootstrap and permutation tests. Show that the bootstrap CI for the **median** has the right coverage by simulation, re-using `mc_mean_ci` from p01.
4. **Multiple testing experiment:** generate 1,000 random "strategies" (iid N(0, 1%) daily returns, 2 years each). How many have a Sharpe > 1 and a p-value < 5%? Apply a Bonferroni correction and the Benjamini–Hochberg procedure. Write it up; this is the most important plot in the project.
5. Regress daily returns on a lagged signal with autocorrelated noise. Show that classical OLS standard errors are too small and Newey–West fixes it.

## Explain it in an interview
- Derive the MLE of a normal's σ². Is it unbiased?
- What does a p-value mean, precisely? And what doesn't it mean?
- You found a strategy with a Sharpe of 1.5 over 1 year. Is it real? What would you need to know?
- When would you trust the bootstrap less? (Think heavy tails and dependence.)
- What assumption behind the OLS standard error fails for overlapping returns?

## Stretch
- Block bootstrap for time series (moving block / stationary bootstrap).
- Ridge and lasso via coordinate descent; plot the regularisation path.
- Implement the **Deflated Sharpe Ratio** (Bailey & López de Prado). You'll need it in p14.

# p12: Statistical Arbitrage via Pairs Trading

**Time:** ~2 weeks · **Language:** Python · **Track weight:** QR ★★★ QT ★★ QD ★

> Correlation is not cointegration. Two random walks can be 90% correlated and drift apart forever.
> This project is about the difference, and about how a mean-reverting spread is modelled, estimated and traded.

## Reading
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) L8, L11, L12 (time series I–III: stationarity, VAR, **cointegration**, state-space models and the **Kalman filter**).
- [18.445](https://ocw.mit.edu/courses/18-445-introduction-to-stochastic-processes-spring-2015/): Markov processes. The Ornstein–Uhlenbeck process is the continuous AR(1).
- Gatev, Goetzmann & Rouwenhorst, *Pairs Trading: Performance of a Relative-Value Arbitrage Rule* (2006).
- Engle & Granger (1987), §1–3.

## What you'll build
[`pairs.py`](pairs.py):
- `hedge_ratio_ols(y, x)`: (α, β) from regressing y on x
- `adf_tstat(series, lags)`: the augmented Dickey–Fuller t-statistic, **from scratch** (an OLS regression you set up yourself)
- `engle_granger(y, x)`: β plus the ADF t-stat of the residual. Compare it to the Engle–Granger 5% critical value of ≈ −3.34, **not** the plain ADF −2.86. Know why.
- `fit_ou(series)`: (κ, μ, σ) via the exact AR(1) discretisation, plus the half-life
- `zscore_positions(spread, window, entry, exit)`: a hysteresis band rule, giving positions in {−1, 0, +1}
- `kalman_hedge_ratio(y, x, delta, obs_var)`: a time-varying β (and α) via a Kalman filter with random-walk state

## Milestones
1. Make the tests pass.
2. On the synthetic market (`../data/synthetic_market.py`), screen **all** pairs with Engle–Granger. How many false positives at 5%? Does it match what multiple testing predicts? (Ground truth is in `mkt.pairs`.)
3. Trade the true pairs with your p11 backtester, using a rolling-OLS hedge ratio and then the Kalman hedge ratio. Include costs, and report Sharpe, turnover and the holding-period distribution.
4. **Out-of-sample discipline:** choose the pairs and parameters on years 1–5 only, then trade them on years 6–10, untouched.
5. Real data: try classic pairs (KO/PEP, XOM/CVX, GLD/GDX, sector ETFs). Document a pair that **broke**, and what a risk manager would have done about it.

## Explain it in an interview
- Explain cointegration to a non-quant in 30 seconds.
- Why does Engle–Granger need different critical values from a plain ADF test?
- Derive the half-life of an AR(1) with coefficient b.
- How do you choose `delta` in the Kalman filter? What does it trade off?
- Why do pairs strategies blow up in crises (e.g. the August 2007 quant quake)?

## Stretch
- Johansen test for baskets of 3+ assets.
- An optimal entry/exit for an OU process (Bertram 2010) compared with your z-score bands.
- PCA residual stat-arb on the full universe (Avellaneda & Lee 2010).

# p11: Event-Driven Backtester

**Time:** ~2 weeks · **Language:** Python (pandas, numpy) · **Track weight:** QR ★★★ QT ★★ QD ★★

> Most backtest bugs make you look *more* profitable, and that's why they survive.
> You'll build a backtester whose design makes lookahead hard to commit, then use it in p12–p16.

## Reading
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) L6 (regression), L8 (time series I).
- [15.401](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/): efficient markets.
- Bailey, Borwein, López de Prado & Zhu, *Pseudo-Mathematics and Financial Charlatanism* (free online).
- López de Prado, *Advances in Financial ML*, ch. 11 ("The Dangers of Backtesting").

## Execution model (the tests enforce it)
- Data: a `DataFrame` of daily close prices (dates × symbols).
- At bar `t`, the strategy sees `prices.iloc[:t+1]` and nothing later, and returns **target positions** in shares.
- Targets decided at bar `t` are **filled at the close of bar `t+1`**. That one-bar delay is the lookahead guard. Targets returned on the last bar are never filled.
- Transaction cost = `cost_bps / 1e4 × |traded notional|`, charged in cash at the fill.
- Equity at bar `t` = cash + Σ position × close, after that bar's fills.
- Short positions are allowed (negative shares) and cash can go negative (leverage). Your risk report should show both.

## What you'll build
[`backtester.py`](backtester.py):
- `run_backtest(prices, strategy, initial_cash, cost_bps) -> BacktestResult` (equity curve, positions, fills, costs)
- `max_drawdown(equity)`, `performance_stats(equity)` (CAGR, annualised vol, Sharpe, max drawdown, Calmar, hit rate)

## Milestones
1. Make the tests pass.
2. Implement three strategies on the synthetic market (`../data/synthetic_market.py`): buy-and-hold equal weight, 12-1 month cross-sectional momentum, and 5-day reversal. Plot the equity curves.
3. **Break it on purpose.** Write a strategy that peeks at tomorrow's price through a global variable. Then add a check that catches it, or explain why it can't be caught in general.
4. Sweep `cost_bps` over 0, 1, 5, 10, 25 for the reversal strategy. At what cost does it die? Plot Sharpe against cost.
5. Vectorise: write a pandas version of the same execution model for target-weight strategies, and confirm it matches the event-driven loop to 1e-10. Compare speed.

## Explain it in an interview
- List five ways a backtest can lie, and the guard against each (lookahead, survivorship, data snooping, costs/slippage, capacity).
- Why fill at the *next* close? What would a more realistic fill model use?
- Your strategy has a Sharpe of 3 in backtest. What do you check first?
- Event-driven vs vectorised backtesting: trade-offs?

## Stretch
- Volume-based slippage model (cost ∝ √(participation rate)).
- Corporate actions: handle splits and dividends from adjusted vs unadjusted prices.
- Plug the p10 feed into a tick-level version.

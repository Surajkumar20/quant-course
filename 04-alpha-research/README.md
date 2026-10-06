# Phase 4: Alpha Research (weeks 27–34)

This is the work a quant researcher actually does: build infrastructure you can trust, form hypotheses, test them honestly, and size positions sensibly.
The main danger in this phase is **fooling yourself** with lookahead bias, overfitting or multiple testing. Every project includes a guard against it.

| Project | Lang | Weeks | OCW backbone |
|---|---|---|---|
| [p11 Event-driven backtester](p11-backtester/) | Python | 27–28 | 18.S096 L6, L8 |
| [p12 Statistical arbitrage: pairs trading](p12-pairs-trading/) | Python | 29–30 | 18.S096 L11–12; 18.445 |
| [p13 Portfolio construction & risk](p13-portfolio-risk/) | Python | 31–32 | 15.401; 18.S096 L7, L14–16; 18.065; 6.079 |
| [p14 ML alpha without fooling yourself](p14-ml-alpha/) | Python | 33–34 | 6.036; 18.650 |

## Data

- **Synthetic first:** [`data/synthetic_market.py`](data/synthetic_market.py) produces a multi-asset daily price panel with a factor structure, a few cointegrated pairs and a *weak planted signal* with known strength. Use it for development, because you know the ground truth.
- **Then real data** (free):
  - daily equity/ETF prices: [Stooq](https://stooq.com/db/h/) bulk downloads, or the `yfinance` package
  - factor returns: the [Kenneth French data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
  - macro series: [FRED](https://fred.stlouisfed.org/)

  Real data has survivorship bias, splits, dividends and missing days. Write down how you handled each.

## The research log

Keep `RESEARCH_LOG.md` in each project folder. **Before** running any backtest, write down the hypothesis, the test, and what result would make you abandon the idea.
Record every variant you try, including failures. You need the count for the multiple-testing correction in p14.

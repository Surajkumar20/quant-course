# p13: Portfolio Construction & Risk

**Time:** ~2 weeks · **Language:** Python · **Track weight:** QR ★★★ QT ★★★ QD ★

> Signals tell you *what* to trade. Portfolio construction tells you *how much*, and that usually matters more.
> Risk tells you what can go wrong, and how likely it is.

## Reading
- [15.401](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/): portfolio theory, CAPM.
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) L7 (Value at Risk), L14 (portfolio theory), L15 (factor modeling), L16 (portfolio management).
- [18.065](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/): SVD/PCA lectures.
- [6.079](https://ocw.mit.edu/courses/6-079-introduction-to-convex-optimization-fall-2009/): quadratic programs and duality (for constrained portfolios).
- Ledoit & Wolf, *A well-conditioned estimator for large-dimensional covariance matrices* (2004).

## What you'll build
[`portfolio.py`](portfolio.py):
- `min_variance_weights`, `mean_variance_weights`, `tangency_weights`: closed forms (derive them with Lagrange multipliers first)
- `ledoit_wolf`: shrinkage toward a scaled identity, with the optimal intensity estimated from data
- `pca(returns, k)`: loadings and explained-variance ratio
- `risk_contributions`, `risk_parity_weights`: equal risk contribution via a simple fixed-point or Newton iteration
- `historical_var`, `historical_es`, `parametric_var`: losses reported as positive numbers

## Milestones
1. Make the tests pass.
2. **Estimation error experiment:** on the synthetic market, compute min-variance portfolios from the sample covariance and from Ledoit–Wolf, using 60, 250 and 1000 days of history. Compare **in-sample against out-of-sample** realised volatility. Plot the gap; it's the main result of this project.
3. PCA: how many factors explain 50% of the variance? Compare the first PC to the market factor in `mkt.factor_returns` (correlation).
4. Build a long-short portfolio from the p14/synthetic signal: dollar-neutral, beta-neutral to PC1, with a gross leverage cap. Use `scipy.optimize.minimize` (or `cvxpy` if you install it). Backtest it with p11.
5. **VaR backtest:** compute rolling 99% 1-day historical VaR and count the breaches. Run a Kupiec test (likelihood ratio). Does normal VaR under-predict with fat tails?

## Explain it in an interview
- Derive the minimum-variance portfolio. Why does it often hold extreme positions in practice?
- Why does the sample covariance matrix fail when the number of assets is close to the number of observations?
- VaR vs Expected Shortfall: why did regulators (FRTB) move to ES?
- What is a risk parity portfolio? Why does it lever up bonds?
- Your portfolio is "market neutral". Name three ways it can still lose a lot of money in a day.

## Stretch
- Black–Litterman with your signal as the "view".
- Hierarchical Risk Parity (López de Prado). Compare its out-of-sample vol to min-variance.
- A transaction-cost-aware rebalance: penalise turnover in the objective.

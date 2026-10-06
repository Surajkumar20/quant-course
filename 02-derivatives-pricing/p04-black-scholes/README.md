# p04: Black–Scholes, Greeks, Binomial Trees & Implied Volatility

**Time:** ~2 weeks · **Language:** Python · **Track weight:** QT ★★★ QR ★★ QD ★★

> In a trading interview you'll be asked for an ATM option's price to within 10% in your head, which delta to hedge with,
> and why a put's gamma equals a call's. This project makes those answers automatic.

## Reading
- [15.401](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/): the options sessions (payoffs, put–call parity, binomial pricing).
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) L5 & L17 (stochastic processes), L18 (Itō calculus), L19 (Black–Scholes, risk-neutral valuation).
- Hull ch. 13 (binomial trees), 15 (BSM), 19 (Greeks). Shreve I ch. 1–4.

## What you'll build
[`pricing.py`](pricing.py):
- `bs_price(S, K, T, r, sigma, q=0, kind="call")`: Black–Scholes–Merton with continuous dividend yield `q`
- `bs_greeks(...)`: a dict with `delta, gamma, vega, theta, rho` (conventions in the docstring)
- `implied_vol(price, S, K, T, r, q=0, kind="call")`: robust. Use Newton with a bisection fallback, and reject prices outside the no-arbitrage bounds.
- `crr_price(S, K, T, r, sigma, steps, q=0, kind="call", american=False)`: Cox–Ross–Rubinstein tree, European or American

## Milestones
1. Derive the BS formula yourself from the risk-neutral expectation E[e^{−rT}(S_T − K)⁺]. Put the derivation in `derivations/`.
2. Implement `bs_price` and check put–call parity numerically on a grid of inputs.
3. Implement `bs_greeks`. Check every Greek against **central finite differences** of `bs_price` in your own tests.
4. Implement `crr_price`. Plot `crr − bs` against steps from 10 to 1000 and explain the **odd/even oscillation**. Then implement the American put and plot the **early-exercise boundary** S*(t).
5. Implement `implied_vol`. Stress-test it: deep ITM/OTM, very short T, prices near the bounds. Count iterations.
6. **Delta-hedging simulation:** simulate GBM paths and hedge a short call daily, then hourly. Plot the P&L distribution. Show that the P&L variance shrinks with hedge frequency, and what happens when realised vol ≠ implied vol.

## Explain it in an interview
- Price an ATM call with S = 100, σ = 20%, T = 3 months, r = 0 in your head. (≈ 0.4·σ√T·S = $4.)
- Why is the gamma of a call equal to that of a put with the same strike?
- Why is it never optimal to exercise an American call early on a non-dividend stock? When is it optimal for a put?
- You're long gamma and delta-hedged. The stock moves 3% today. Did you make or lose money? What did you pay for that?
- What does implied vol represent? Why isn't it the same across strikes?

## Stretch
- Leisen–Reimer tree (much faster convergence). Compare convergence plots.
- Vectorise `bs_price` and `implied_vol` over numpy arrays: 10⁶ implied vols in under 1 second.
- Jäckel's "Let's Be Rational" implied vol algorithm.
- Digital options and their Greeks. Why is a digital hard to hedge near expiry?

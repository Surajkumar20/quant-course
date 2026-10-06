# Phase 2: Derivatives Pricing (weeks 12–20)

This phase is the core of the bank quant role, and options intuition matters for trading roles too. You price the same instrument four different ways and make them agree.

| Project | Lang | Weeks | OCW backbone |
|---|---|---|---|
| [p04 Black–Scholes, Greeks, trees, implied vol](p04-black-scholes/) | Python | 12–13 | 15.401, 18.S096 L17–19 |
| [p05 Monte Carlo pricer](p05-monte-carlo-pricer/) | C++ | 14–15 | 18.S096 L19–21, 6.172 |
| [p06 Volatility surface & SVI](p06-vol-surface/) | Python | 16–17 | 18.S096 L9, L20 |
| [p07 Finite-difference PDE pricer](p07-pde-pricer/) | C++ | 18–20 | 18.085, 18.086, 18.S096 L19 |

**The test of this phase:** given (S, K, T, r, σ), you get the same European put price from the closed form (p04), a binomial tree (p04), Monte Carlo with an error bar (p05) and a PDE grid (p07), and you can explain every discrepancy.

**Before you start:** read Hull ch. 10–15 (option properties, trees, Black–Scholes–Merton, Greeks) and Shreve Vol I ch. 1–2.

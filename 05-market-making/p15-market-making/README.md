# p15: Market-Making Simulator (Avellaneda–Stoikov)

**Time:** ~2 weeks · **Language:** Python · **Track weight:** QT ★★★ QR ★★ QD ★★

> Quoting tight earns spread but loads you with inventory. Quoting wide is safe but nobody trades with you.
> Avellaneda–Stoikov (2008) turns that trade-off into a stochastic control problem, and the answer is surprisingly simple.

## Reading
- Avellaneda & Stoikov, *High-frequency trading in a limit order book* (Quantitative Finance, 2008). It's short; read all of it.
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) L5 & L17 (stochastic processes). The HJB intuition behind optimal control.
- [14.16 Strategy and Information](https://ocw.mit.edu/courses/14-16-strategy-and-information-spring-2016/): adverse selection, and why the market maker loses to informed traders (Glosten–Milgrom, Kyle).
- Cartea, Jaimungal & Penalva, *Algorithmic and High-Frequency Trading*, ch. 10.
- Guéant, Lehalle & Fernandez-Tapia (2013) on inventory limits (stretch).

## Model
- Mid price: arithmetic Brownian motion, simulated as ±σ√dt steps.
- You post a bid at depth δᵇ = s − bid and an ask at δᵃ = ask − s.
- Market orders hit you as Poisson arrivals with intensity λ(δ) = A·e^{−kδ}, so the fill probability in dt is 1 − e^{−λ(δ)dt}.
- Exponential utility with risk aversion γ, horizon T.

Results you'll implement:
- reservation price r = s − q·γ·σ²·(T − t)
- optimal total spread δᵃ + δᵇ = γσ²(T − t) + (2/γ)·ln(1 + γ/k)

## What you'll build
[`mm.py`](mm.py):
- `reservation_price`, `optimal_spread`, `as_quotes`, `fill_probability`
- `simulate(strategy, ...)`: an event loop returning P&L, inventory path and fill counts. A strategy is any `f(t, s, q) -> (bid, ask)`.

## Milestones
1. Make the tests pass.
2. Reproduce **Table 1 / Figure 2** of the Avellaneda–Stoikov paper: the inventory strategy against the symmetric strategy over 1,000 simulations, for γ ∈ {0.01, 0.1, 0.5}. Report mean P&L, std P&L, mean |final q|.
3. **Adverse selection:** add informed flow. With probability α, a market order comes from a trader who knows the mid's next move and trades only in that direction. Plot P&L against α. At what α does the market maker stop making money? How should the spread respond?
4. **Inventory limits:** stop quoting the side that would breach |q| ≤ Q_max. Compare with AS.
5. Replace ABM with mid prices from your p10 feed or the p11 synthetic market. Does the model still behave?

## Explain it in an interview
- Why does the reservation price shift *against* your inventory? Explain it without equations.
- What happens to the optimal spread as γ → 0? As T − t → 0?
- What is adverse selection? Why does a market maker widen out before earnings or economic releases?
- You're long 500 lots and the market starts ticking down. Walk through what you do.
- How would you estimate A and k from real order-book data?

## Stretch
- The Guéant–Lehalle–Fernandez-Tapia closed-form approximation with inventory bounds.
- Multi-level quoting (several price levels per side).
- Rebuild the simulator as a C++ strategy that consumes your p10 feed and sends orders into your p08 matching engine.

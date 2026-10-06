# p06: Volatility Surface & SVI Calibration

**Time:** ~2 weeks · **Language:** Python (numpy, scipy.optimize) · **Track weight:** QT ★★★ QR ★★★ QD ★

> Black–Scholes says implied vol is flat. It isn't. Every options desk keeps a vol surface, and the model
> it uses must fit the market **without creating arbitrage**. This project builds one.

## Reading
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) L9 (volatility modeling), L20 (option price & probability duality, i.e. Breeden–Litzenberger).
- [18.642 (Fall 2024)](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024): the newer treatment of the same material.
- Gatheral, *The Volatility Surface*, ch. 1–3.
- Gatheral & Jacquier, *Arbitrage-free SVI volatility surfaces* (2014, free on arXiv). Read §2–4.

## Notation
- log-moneyness k = ln(K / F_T), where F_T is the forward
- total implied variance w(k, T) = σ_imp(k, T)² · T
- raw SVI: w(k) = a + b(ρ(k − m) + √((k − m)² + σ²))

## What you'll build
[`vol_surface.py`](vol_surface.py):
- `svi_total_variance`, `svi_derivatives` (w, w′, w″ analytically)
- `butterfly_g(k, params)`: Gatheral's density function g(k). There is **no butterfly arbitrage** iff g ≥ 0.
- `has_butterfly_arbitrage`, `has_calendar_arbitrage` (total variance must be non-decreasing in T at every k)
- `svi_density(k, params)`: the risk-neutral density of k implied by the smile. It must integrate to 1.
- `fit_svi(k, w, ...)`: least-squares calibration with sensible bounds and a good initial guess

[`data/generate_chain.py`](data/generate_chain.py) (provided, complete) writes a synthetic option chain with bid/ask quotes across 6 expiries. You turn quotes into a surface.

## Milestones
1. Run the generator. Compute mid prices, back out implied vols with **your p04 `implied_vol`** (copy the module in), and plot the smiles. Use OTM options only. Why?
2. Implement SVI and its derivatives. Check w′ and w″ against finite differences.
3. Implement `butterfly_g`. Reproduce the Gatheral–Jacquier counterexample (in the tests) and plot g(k) going negative. Then plot the negative density it implies.
4. Implement `fit_svi`. Fit each expiry, then plot fitted against market vols, with residuals in vol points.
5. Check the fitted surface for calendar arbitrage. If you find any, fix it (constrained fit, or re-fit expiries in sequence).
6. **Real data:** download a delayed option chain (e.g. CBOE delayed quotes for SPX/SPY), and repeat 1–5. Real data has crossed quotes, zero bids and stale strikes. Document your cleaning rules.

## Explain it in an interview
- Why does equity index implied vol show a **skew** (OTM puts expensive)? Why do FX smiles look different?
- What is butterfly arbitrage in terms of option prices? (Convexity in strike.) And calendar arbitrage?
- How does the risk-neutral density relate to ∂²C/∂K²?
- Sticky-strike vs sticky-delta: the spot moves 1%, so what happens to the ATM vol you quote?

## Stretch
- SSVI (surface SVI) with guaranteed no-calendar-arbitrage parameterisation.
- Calibrate Heston to the surface (characteristic function + FFT/quadrature pricing).
- Local vol via Dupire's formula from your SVI surface. Price a barrier with it in p05 and compare to flat-vol BS.

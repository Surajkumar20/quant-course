# p05: Monte Carlo Option Pricer in C++

**Time:** ~2 weeks · **Language:** C++20 · **Track weight:** QD ★★★ QR ★★ QT ★★

> A Monte Carlo price without a standard error is meaningless. A Monte Carlo engine that isn't reproducible
> can't be debugged. A Monte Carlo engine that doesn't use variance reduction wastes the firm's compute.

## Reading
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) L19 (risk-neutral valuation), L20 (option price & probability duality), L21 (SDEs).
- [6.172](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/) L1–2 (performance, Bentley rules), L6 (multicore programming).
- Glasserman, *Monte Carlo Methods in Financial Engineering*, ch. 1, 3.1–3.2 (path generation), 4.1–4.2 (antithetics, control variates).
- Joshi, *C++ Design Patterns and Derivatives Pricing*, ch. 1–6.

## What you'll build
[`include/mc.hpp`](include/mc.hpp) (API) and [`src/mc.cpp`](src/mc.cpp) (stubs). The model is GBM under the risk-neutral measure:
S_T = S_0 · exp((r − q − σ²/2)T + σ√T·Z).

| Function | What |
|---|---|
| `bs_price` | closed form (reference for tests; port it from p04) |
| `price_european` | plain MC, optional **antithetic** variates |
| `price_european_cv` | **control variate** using S_T, whose expectation is known |
| `price_asian` | discretely monitored arithmetic or geometric average; optional geometric **control variate** for the arithmetic option |
| `asian_geometric_closed_form` | closed form for the discrete geometric Asian (derive it!) |
| `price_up_and_out_call` | discretely monitored barrier |
| `price_european_mt` | multi-threaded with `std::thread`, using **independent RNG streams** per thread |

Every function returns `Result{price, std_error, n_paths}`.

## Milestones
1. `bs_price` + `price_european`. Plot price ± 2 SE against n_paths and verify the 1/√n shrinkage.
2. Antithetics and control variates. Report the **variance reduction factor** for each (ATM, ITM, OTM).
3. Derive the geometric-Asian closed form (log of a product of lognormals). Use it as a control variate for the arithmetic Asian. Expect a > 50× variance reduction.
4. Barrier: plot the discretely monitored price against `n_steps` and compare to the continuous-monitoring closed form (Hull, "Exotic Options" chapter, barrier options). Explain the bias, then look up the Broadie–Glasserman–Kou correction.
5. Multi-threading: measure speed-up for 1, 2, 4, 8 threads. Explain why seeding every thread with the same seed is a **bug**, and why `seed + thread_id` with mt19937 is only "probably fine".
6. Profile (perf / VTune / Instruments). Where does the time go: RNG, `exp`, or memory?

## Explain it in an interview
- Why does antithetic sampling work for a call but do almost nothing for a straddle?
- What makes a good control variate? Derive the optimal coefficient b*.
- Why is MC preferred over PDEs for path-dependent and high-dimensional problems?
- How would you compute delta by MC? Compare bump-and-reprice with common random numbers against the pathwise and likelihood-ratio estimators.
- How do you make a parallel MC run reproducible regardless of thread count?

## Stretch
- Quasi-random Sobol sequences with a Brownian bridge. Compare convergence rates.
- Pathwise delta and likelihood-ratio delta for the digital option.
- Basket option on 5 correlated assets, using your p02 Cholesky.
- Longstaff–Schwartz for the American put. Compare to your p04 tree.

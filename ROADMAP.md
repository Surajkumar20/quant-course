# Roadmap

The pacing assumes **~20 hours/week** alongside other commitments, which comes to about **40 weeks**. At full time (40+ h/week) it takes about 20 weeks.
Each week is roughly half OCW lectures and problem sets and half building.

## Pick a track (you can change later)

| Track | What the job is | Weight these projects | Interview emphasis |
|---|---|---|---|
| **QR**: Quant Researcher | Find and validate predictive signals and models | p01, p03, p06, p11–p14, p16 | stats, probability, ML, research design |
| **QT**: Quant Trader | Price, quote and manage risk in real time | p01, p04, p05, p13, p15, drills | mental math, probability, betting/market games |
| **QD**: Quant Developer | Build the pricing libraries and the low-latency trading stack | p02, p05, p07–p10, p16 | C++, data structures, systems, concurrency |

Do **every** project anyway. A QD who can't price an option, or a QR who can't write C++, is a weaker candidate.

---

## Phase 0: Precourse (weeks 1–4)
Folder: [`00-precourse`](00-precourse/)

| Week | OCW / reading | Build |
|---|---|---|
| 1 | Missing Semester (shell, git, editors, debugging) | p00 toolchain; set up your fork and CI |
| 2 | 6.100L lectures 1–12 *or* skim if you're comfortable in Python; 6.S096 (C/C++) lectures 1–4 | diagnostic, part A |
| 3 | 18.06 lectures 1–10 (review); 18.600 lectures 1–10 (review) | diagnostic, part B |
| 4 | 6.006 lectures 1–8 (review) | start daily mental-math drills (`drills/mental_math.py`) and keep them going for the rest of the course |

**Gate:** score ≥ 70% on the [diagnostic](00-precourse/diagnostic.md). If you don't, spend two more weeks on the weakest area.

## Phase 1: Foundations (weeks 5–11)
Folder: [`01-foundations`](01-foundations/)

| Week | OCW | Build |
|---|---|---|
| 5–6 | 18.600 (all of it: conditional expectation, martingale intuition, limit theorems) | **p01** Monte Carlo probability lab (Py) |
| 7–8 | 18.06 (LU, QR, eigen, SVD) + 6.S096 C++ | **p02** Matrix library (C++) |
| 9–11 | 18.650 (MLE, tests, regression, bootstrap) | **p03** Statistics toolkit (Py) |

## Phase 2: Derivatives pricing (weeks 12–20)
Folder: [`02-derivatives-pricing`](02-derivatives-pricing/)

| Week | OCW | Build |
|---|---|---|
| 12–13 | 15.401 (options, arbitrage); 18.S096 L5 & L17 (stochastic processes), L18 (Itō calculus), L19 (Black–Scholes, risk-neutral valuation) | **p04** Black–Scholes, Greeks, binomial trees, implied vol (Py) |
| 14–15 | 18.S096 L20–21 (option price/probability duality, SDEs); 6.172 L1–2 (intro, Bentley rules) | **p05** Monte Carlo pricer with variance reduction and threads (C++) |
| 16–17 | 18.S096 L9 (volatility modeling); Gatheral ch. 1–3 | **p06** Volatility surface & SVI calibration (Py) |
| 18–20 | 18.085 (finite differences); 18.086 (PDEs, stability) | **p07** Crank–Nicolson / PSOR PDE pricer (C++) |

## Phase 3: Low-latency systems (weeks 21–26)
Folder: [`03-low-latency-systems`](03-low-latency-systems/)

| Week | OCW | Build |
|---|---|---|
| 21–22 | 6.006 (heaps, hashing, balanced BSTs); 6.172 (cache, bit hacks) | **p08** Limit order book & matching engine (C++) |
| 23–24 | 6.172 L6–7 (multicore, races), L16–17 (nondeterministic programming, synchronization without locks); 6.004 (memory hierarchy) | **p09** Lock-free SPSC ring buffer (C++) |
| 25–26 | 6.172 L10 (measurement & timing), L14 (caching) | **p10** Binary market-data feed handler (C++) |

## Phase 4: Alpha research (weeks 27–34)
Folder: [`04-alpha-research`](04-alpha-research/)

| Week | OCW | Build |
|---|---|---|
| 27–28 | 18.S096 L6 (regression), L8 (time series I) | **p11** Event-driven backtester (Py) |
| 29–30 | 18.S096 L11–12 (time series II–III: cointegration, state-space/Kalman); 18.445 (Markov processes) | **p12** Statistical arbitrage: pairs trading (Py) |
| 31–32 | 15.401 (portfolio theory, CAPM); 18.S096 L7 (VaR), L14–16 (portfolio theory, factor modeling, portfolio management); 18.065 (PCA) | **p13** Portfolio construction & risk (Py) |
| 33–34 | 6.036 (supervised learning, regularization, CV) | **p14** ML alpha without fooling yourself (Py) |

## Phase 5: Market making (weeks 35–36)
Folder: [`05-market-making`](05-market-making/)

| Week | OCW | Build |
|---|---|---|
| 35–36 | 18.S096 L5 & L17 (stochastic processes); 14.16 (strategy & information: adverse selection, auctions) | **p15** Market-making simulator (Py) |

## Phase 6: Capstone (weeks 37–40+)
Folder: [`06-capstone`](06-capstone/)

**p16**: C++ matching engine and feed → Python research → strategy → backtest → risk report, written up like a short paper. This is the project you lead with on your résumé.

---

## Running in parallel the whole time

- **Mental math:** 10 min/day with `00-precourse/drills/mental_math.py`. Aim for 80 correct in 8 minutes.
- **Probability puzzles:** 3/week from [`resources/interview-prep.md`](resources/interview-prep.md).
- **LeetCode-style DSA:** 3/week, medium difficulty, in C++. QD candidates should do 5/week.
- **Markets:** read the *FT* or *Matt Levine's Money Stuff* daily. Being able to say why a price moved is a skill interviewers check for.

# Phase 6: Capstone (weeks 37–40+)

# p16: End-to-End Trading System + Research Paper

**Time:** 4–6 weeks · **Languages:** C++ (engine) + Python (research) · **This is the project you lead with in interviews.**

You've built every component. Now connect them into a system, run a real piece of research on top of it, and write it up the way a research desk would.
There are no stub files or provided tests here. You write the spec, and the tests are yours too.

## The system

```
                 ┌──────────────────────┐
 gen_feed.py ──► │ p10 feed handler     │  (C++, thread 1)
  or real ITCH   │ parse → book events  │
                 └─────────┬────────────┘
                           │ p09 SPSC queue
                 ┌─────────▼────────────┐
                 │ book builder +       │  (C++, thread 2)
                 │ strategy (p15 MM or  │
                 │ your p14 signal)     │
                 └─────────┬────────────┘
                           │ orders (p09 SPSC queue)
                 ┌─────────▼────────────┐
                 │ p08 matching engine  │  (C++, thread 3, simulated exchange)
                 └─────────┬────────────┘
                           │ fills, logged to binary/CSV
                 ┌─────────▼────────────┐
                 │ Python research:     │
                 │ p11 analytics, p13   │
                 │ risk, p14 validation │
                 └──────────────────────┘
```

## Choose a track

| Track | Core deliverable |
|---|---|
| **QD** | Make the C++ pipeline above fast and correct. Target: replay 10M messages end to end, with p50/p99 **tick-to-order latency** measured per message and a flame graph showing where the time goes. |
| **QT** | Run your p15 market maker inside the C++ pipeline against simulated flow that includes informed traders. Tune it (spread, skew, inventory limits) and show its P&L attribution: spread capture vs. adverse selection vs. inventory. |
| **QR** | Take a signal from idea to deflated Sharpe on **real** daily data (Stooq/yfinance): features → purged CV → portfolio (p13) → backtest with costs (p11) → DSR (p14) → a capacity estimate. |

Whichever track you pick, you still deliver the **minimum system**: feed → book → strategy → orders → fills → Python analysis, working end to end, even if one part is simple.

## Deliverables

1. **`DESIGN.md`** (before you code): goals, non-goals, components, interfaces, test plan, and the risks you expect.
2. **Code** with tests: unit tests per component, plus at least one **end-to-end test** that replays a small fixed feed and checks the exact fills.
3. **`PAPER.md`**, 4–6 pages, structured like a short research note:
   - Abstract (5 sentences)
   - Question & hypothesis
   - Data & methodology, including every choice that could bias the result
   - Results: tables and figures with error bars
   - Robustness: what breaks it? (parameter sensitivity, sub-periods, costs)
   - Limitations & next steps
4. **A 10-minute talk**, recorded. Present it to your study group and take questions.

## Rubric (self-assessment; be honest)

| | 1: weak | 3: solid | 5: hire-worthy |
|---|---|---|---|
| Correctness | tests sparse or failing | good unit tests | unit + e2e + randomised/property tests, sanitizers clean |
| Performance (QD) | not measured | measured averages | percentiles, flame graphs, before/after for each optimisation |
| Research rigour (QR/QT) | in-sample only | out-of-sample | purged CV, DSR, costs, sub-period and parameter robustness |
| Communication | code only | README | paper + talk that a PM could act on |
| Independence | heavy AI use | some AI | AI log shows only conceptual questions |

## Then: apply

- Put the capstone first on your résumé, with one line and one number (e.g. "C++ feed handler + matching engine, 8M msgs/s, p99 tick-to-order 2.1 µs").
- Your GitHub fork is your portfolio. Pin the capstone and make sure the README of your fork summarises what you built and links each `WRITEUP.md`.
- Do one mock interview per week from [`resources/interview-prep.md`](../resources/interview-prep.md) until your interviews.

# Phase 3: Low-Latency Systems (weeks 21–26)

This is the infrastructure of electronic trading. It's the core of the QD interview at HFT firms, and QR/QT candidates who understand it stand out.

| Project | Lang | Weeks | OCW backbone |
|---|---|---|---|
| [p08 Limit order book & matching engine](p08-order-book/) | C++ | 21–22 | 6.006, 6.172 L1–2, L14 |
| [p09 Lock-free SPSC queue](p09-spsc-queue/) | C++ | 23–24 | 6.172 L6–7, L16–17; 6.004 |
| [p10 Binary market-data feed handler](p10-feed-handler/) | C++ | 25–26 | 6.172 L10, L14 |

**Read alongside:** Larry Harris, *Trading and Exchanges* (ch. 1–7). Watch the CppCon talks by Carl Cook ("When a Microsecond Is an Eternity") and David Gross ("Trading at Light Speed").

**Rules for this phase:**
- Correct first, then measure, then optimise. Every optimisation claim needs a benchmark number **before and after**.
- Report latency as **percentiles** (p50/p99/p99.9), not averages.
- Run the tests under ASan/UBSan (`-DQC_SANITIZE=ON`). For p09, also run them under ThreadSanitizer (`-fsanitize=thread`).

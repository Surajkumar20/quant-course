# Quant Course

A free, project-based path to a job as a **quant researcher, quant trader, or quant developer**.
It is built on **MIT OpenCourseWare**, and you write the projects in **Python and C++**.

The bar is a front-office quant seat at a large NYC bank, or at a prop/HFT firm such as Jane Street, Citadel Securities, HRT, Jump, Optiver, SIG or Two Sigma.
The material is roughly what a strong CMU or MIT graduate knows walking in. Here you build it, not just read it.

> **Fork it. Do the work yourself. Use as little AI as possible.**
> Someone who gets through these projects mostly unaided is rare. Interviewers can tell who that is within ten minutes.

---

## How it works

1. **Fork** this repo and clone your fork.
2. Do [`00-precourse`](00-precourse/) first. It is the floor, not optional reading.
3. Work through the phases in order. Each project folder contains:
   - `README.md`: context, the MIT OCW readings, the spec, milestones and stretch goals
   - starter code with **stubs** (`raise NotImplementedError` / `throw std::logic_error`)
   - **tests** that fail until your implementation is correct
4. A project is done when it meets the [Definition of Done](RULES.md#definition-of-done). Passing the tests is only one part of that.
5. Record your progress in [`PROGRESS.md`](PROGRESS.md) and turn the project on in CI by adding its path to [`tools/enabled_projects.txt`](tools/enabled_projects.txt).

Read **[RULES.md](RULES.md)** before you start. It covers the AI policy, the 30-minute rule and the journal.

## The map

| Phase | Theme | Projects | Lang | Main MIT OCW backbone |
|---|---|---|---|---|
| **0** | [Precourse](00-precourse/) | toolchain, diagnostics, mental-math drills | Py + C++ | Missing Semester, 6.100L, 18.06, 18.600 |
| **1** | [Foundations](01-foundations/) | probability by simulation, matrix library, statistics toolkit | Py + C++ | 18.600, 18.06, 18.650, 6.S096 |
| **2** | [Derivatives pricing](02-derivatives-pricing/) | Black–Scholes & trees, MC pricer, vol surface, PDE solver | Py + C++ | 18.S096, 15.401, 18.085/086 |
| **3** | [Low-latency systems](03-low-latency-systems/) | order book, lock-free queue, binary feed handler | C++ | 6.172, 6.004, 6.006 |
| **4** | [Alpha research](04-alpha-research/) | backtester, stat-arb, portfolio & risk, ML without fooling yourself | Py | 18.S096, 18.650, 15.401, 6.036 |
| **5** | [Market making](05-market-making/) | Avellaneda–Stoikov market-maker simulator | Py | 18.S096, 18.445, 14.16 |
| **6** | [Capstone](06-capstone/) | end-to-end trading system plus a research write-up | Py + C++ | all of the above |

Week-by-week pacing and which track (QR / QT / QD) each project matters most for are in **[ROADMAP.md](ROADMAP.md)**.

## Resources

- [`resources/mit-ocw.md`](resources/mit-ocw.md): every MIT OCW course used here, and which lectures matter
- [`resources/books.md`](resources/books.md): the short list of books worth owning
- [`resources/interview-prep.md`](resources/interview-prep.md): probability puzzles, market-making games, mental math, and how the interview loops actually run

## Repo layout

```
00-precourse/            setup, diagnostic, drills
01-foundations/          p01–p03
02-derivatives-pricing/  p04–p07
03-low-latency-systems/  p08–p10
04-alpha-research/       p11–p14
05-market-making/        p15
06-capstone/             p16
resources/               OCW map, books, interview prep
templates/               journal + project write-up templates
tools/                   test runner, CI project list
CMakeLists.txt           builds every C++ project (GoogleTest via FetchContent)
pyproject.toml           Python deps + pytest config
```

## Quick start

```bash
# Python (3.11+)
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python tools/run_tests.py 00-precourse/p00-toolchain

# C++ (C++20 compiler + CMake 3.20+)
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
ctest --test-dir build -R p00 --output-on-failure
```

## Why one repo, and why folders instead of branches

Everything is on `main` in plain folders. GitHub forks copy **only the default branch** unless you untick a box, so material kept on other branches is easy to lose without noticing. Folders also make the whole course greppable and diffable.
Branches belong to **you**: work on `p04-black-scholes` and merge to `main` once it meets the Definition of Done. That way your fork's history shows how your work progressed.

## License

The code and text here are MIT licensed (see [LICENSE](LICENSE)). MIT OpenCourseWare material is only **linked**, never copied. It is © MIT and licensed CC BY-NC-SA 4.0.
This project is not affiliated with MIT or any firm named above.

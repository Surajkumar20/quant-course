# Phase 0: Precourse (weeks 1–4)

This phase covers what a strong CS / math / physics graduate from CMU or MIT already knows on their first day.
If you're coming from somewhere else, this is where you catch up. It's not optional: everything later assumes it.

## Checklist

### Tools (week 1)
- [ ] Work through [Missing Semester](https://missing.csail.mit.edu/): shell, shell tools, editors, data wrangling, command-line environment, version control, debugging & profiling.
- [ ] You can use `git` from the command line: branch, commit, rebase, resolve a merge conflict, and open a PR on your fork.
- [ ] A C++20 compiler works (GCC ≥ 11, Clang ≥ 14 or MSVC 2022) along with CMake ≥ 3.20.
- [ ] Python ≥ 3.11 is installed in a virtual environment with `requirements.txt`.
- [ ] Your editor has autocomplete AI **off** for this repo (see [RULES.md](../RULES.md)).
- [ ] **[p00-toolchain](p00-toolchain/)** passes in both languages.

### Python (week 2)
Source: [6.100L](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/). If you're already fluent, do the last 3 problem sets only.
- [ ] list/dict/set comprehensions, generators, `dataclasses`, type hints
- [ ] numpy: broadcasting, vectorisation, and why a Python `for` loop over 10⁶ elements is slow
- [ ] pandas: indexing, `groupby`, `rolling`, `merge`, time-series resampling
- [ ] matplotlib: line, scatter, histogram, and subplots with labelled axes

### C++ (week 2)
Source: [6.S096 Effective Programming in C and C++](https://ocw.mit.edu/courses/6-s096-effective-programming-in-c-and-c-january-iap-2014/) plus Stroustrup's *A Tour of C++*.
- [ ] stack vs heap, RAII, `std::unique_ptr`, rule of 0/3/5
- [ ] references, `const` correctness, move semantics
- [ ] `std::vector`, `std::unordered_map`, `std::map`, iterators, `<algorithm>`
- [ ] templates (basic), lambdas
- [ ] build with CMake; run under a debugger (gdb/lldb/VS) and a sanitizer (`-DQC_SANITIZE=ON`)

### Math (week 3)
- [ ] **Linear algebra** ([18.06SC](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) units I–II as review): Gaussian elimination, rank, null space, orthogonality, least squares, eigenvalues.
- [ ] **Probability** ([18.600](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/) first third as review): counting, conditional probability, Bayes, discrete and continuous random variables, expectation, variance.
- [ ] **Calculus** ([18.02SC](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/) as needed): partial derivatives, gradients, Taylor expansion, double integrals, Lagrange multipliers.

### Algorithms (week 4)
Source: [6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) lectures 1–8 as review.
- [ ] Big-O, arrays vs linked lists, hashing, heaps, BSTs, sorting, BFS/DFS

### Markets vocabulary (all month)
Source: [18.S096 Lecture 1](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) and [15.401](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/) sessions 1–4.
- [ ] Explain in your own words: bid/ask, spread, market vs limit order, long/short, leverage, a stock vs a future vs an option, present value, arbitrage, market maker vs taker.

## Gate

Take the **[diagnostic](diagnostic.md)** under exam conditions: 2 hours, no notes, no AI.
Score **≥ 70%** before starting Phase 1. If you don't, spend two more weeks on your weakest section and retake it.

## Start these habits now
- `python 00-precourse/drills/mental_math.py` for 10 min/day (see [interview-prep](../resources/interview-prep.md#mental-math))
- 3 probability puzzles/week
- 3 LeetCode mediums/week, in C++

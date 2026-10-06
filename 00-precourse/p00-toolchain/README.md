# p00: Toolchain & Time Value of Money

**Time:** 2–4 hours · **Languages:** Python + C++ · **Reading:** [15.401](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/) sessions 2–3 (present value)

The point of this project is to prove your setup works end to end: venv, pytest, CMake, GoogleTest, git branch, CI.
Along the way you implement the most basic idea in finance: **a dollar today is worth more than a dollar tomorrow.**

## Spec

Implement the same four functions in both languages.

| Function | Meaning |
|---|---|
| `future_value(pv, rate, n)` | value after `n` periods of compounding at `rate` per period |
| `present_value(fv, rate, n)` | inverse of the above |
| `npv(rate, cashflows)` | Σ cashflows[t] / (1+rate)^t, with t starting at **0** |
| `irr(cashflows)` | the rate r with npv(r, cashflows) = 0. Use **bisection** on [-0.99, 10]; raise/throw if there's no sign change |

- Python: [`tvm.py`](tvm.py), tests in [`tests/test_tvm.py`](tests/test_tvm.py)
- C++: [`include/tvm.hpp`](include/tvm.hpp), [`src/tvm.cpp`](src/tvm.cpp), tests in [`tests/test_tvm.cpp`](tests/test_tvm.cpp)

## Milestones

1. `python tools/run_tests.py 00-precourse/p00-toolchain` fails, and you understand every failure message.
2. Make the Python tests pass.
3. Make the C++ tests pass (`ctest --test-dir build -R ^p00_ --output-on-failure`).
4. Add `00-precourse/p00-toolchain` to `tools/enabled_projects.txt`, push, and see green CI on your fork.
5. Break a test on purpose, push, see red CI, then fix it. You now trust your feedback loop.

## Explain it in an interview
- Why does bisection always converge here, and how many iterations does it take to reach 1e-10 tolerance?
- When can a cash-flow stream have **more than one** IRR? Give an example.
- Why would you use Newton's method instead, and when does it fail?

## Stretch
- Implement `irr` with Newton's method, falling back to bisection. Count iterations for both.
- Write a C++ microbenchmark comparing `std::pow` against repeated multiplication in `npv`.

## Troubleshooting

- **Windows: `CMake Error ... CompilerIdC/a.exe cannot be read`.** Antivirus is usually locking freshly built executables while CMake inspects them. A trivial hello-world project fails the same way. In order of preference, fix it by:
  1. adding your clone's `build/` folder to your antivirus exclusions,
  2. using WSL2 (Ubuntu) for the C++ work, which is also closer to what trading firms run, or
  3. telling CMake to skip compiler identification:
     ```
     cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_C_COMPILER_ID_RUN=1 -DCMAKE_CXX_COMPILER_ID_RUN=1 ^
       -DCMAKE_C_COMPILER_ID=GNU -DCMAKE_CXX_COMPILER_ID=GNU ^
       -DCMAKE_C_COMPILER_VERSION=13.2.0 -DCMAKE_CXX_COMPILER_VERSION=13.2.0 ^
       -DCMAKE_C_STANDARD_COMPUTED_DEFAULT=17 -DCMAKE_C_EXTENSIONS_COMPUTED_DEFAULT=ON ^
       -DCMAKE_CXX_STANDARD_COMPUTED_DEFAULT=17 -DCMAKE_CXX_EXTENSIONS_COMPUTED_DEFAULT=ON
     ```
     Replace 13.2.0 with your `gcc --version`.
- **First configure is slow.** CMake downloads GoogleTest once. You need to be online for that.

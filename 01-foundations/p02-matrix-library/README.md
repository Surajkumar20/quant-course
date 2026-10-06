# p02: Dense Matrix Library in C++

**Time:** ~2 weeks · **Language:** C++20 · **Track weight:** QD ★★★ QR ★★ QT ★

> You will use Eigen or numpy in real work. You write this so you know what they are doing,
> and so that "implement LU" or "why is this matrix multiply slow?" doesn't throw you in an interview.

## Reading
- [18.06SC](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) Unit I (elimination, LU, permutations, inverses, determinants) and Unit II (least squares, orthogonality, QR).
- [6.S096](https://ocw.mit.edu/courses/6-s096-effective-programming-in-c-and-c-january-iap-2014/): classes, operator overloading, `const`, RAII.
- [6.172](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/) Lecture 1 (matrix multiply from 21 hours down to milliseconds) and Lecture 14 (caching).
- [18.335J](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/) on pivoting and stability (stretch).

## What you'll build
[`include/matrix.hpp`](include/matrix.hpp) declares the API and [`src/matrix.cpp`](src/matrix.cpp) holds the stubs.
- `Matrix`: row-major `std::vector<double>` storage, `operator()`, `transpose`, `+ - *`, scalar multiply, matrix-vector product
- `lu_decompose`: LU **with partial pivoting**, returning the packed LU, the permutation and its sign
- `solve`, `determinant`, `inverse` built on top of LU
- `cholesky`: for symmetric positive-definite matrices (correlation and covariance matrices in p05 and p13)
- `least_squares`: via QR (Householder) or the normal equations. Implement **both** and compare their accuracy.

Rules: throw `std::invalid_argument` on dimension mismatch and `std::domain_error` on a singular or non-SPD input.

## Milestones
1. `Matrix` basics pass their tests.
2. LU + solve + det + inverse pass, including the random 60×60 residual test.
3. Cholesky passes. Use it to generate correlated normals (Z → LZ) and check the sample correlation.
4. **Performance:** fill in [`bench/bench_matmul.cpp`](bench/bench_matmul.cpp). Time naive `ijk`, then `ikj`, then a blocked/tiled version, for n = 256, 512 and 1024. Plot GFLOP/s.
   Explain the difference using cache lines. Then build with `-O0` against `-O3 -march=native` and compare.
5. Run the tests under sanitizers: `cmake -B build-asan -DQC_SANITIZE=ON` (GCC/Clang).

## Explain it in an interview
- Why does Gaussian elimination need pivoting? Give a 2×2 example where it fails without it.
- Cost of LU vs. cost of solving once you have LU. Why factor once and solve many times?
- Why is `ikj` faster than `ijk` for row-major storage?
- Why use Cholesky to simulate correlated Brownian motions? What happens if the matrix isn't PSD?
- Normal equations vs QR: which is more accurate and why? (Think condition numbers.)

## Stretch
- Template it as `Matrix<T>` and test with `float` vs `double` precision.
- Add expression templates so `A + B + C` allocates once.
- Parallelise the blocked matmul with `std::thread` and measure speed-up up to your core count.
- Compare your solver against Eigen.

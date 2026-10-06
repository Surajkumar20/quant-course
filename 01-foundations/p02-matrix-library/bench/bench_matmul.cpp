// Matrix-multiply benchmark harness. Run: ./build/01-foundations/p02-matrix-library/p02_bench
//
// Milestone 4: implement the three kernels below, then report GFLOP/s (2 n^3 flops / time)
// for n = 256, 512, 1024 in your WRITEUP.md.
#include <chrono>
#include <cstdio>
#include <random>
#include <vector>

using Kernel = void (*)(const double* a, const double* b, double* c, int n);

// c = a * b, all n x n row-major. c is zero on entry.
void matmul_ijk(const double* /*a*/, const double* /*b*/, double* /*c*/, int /*n*/) {
    // TODO: textbook triple loop, i then j then k
}

void matmul_ikj(const double* /*a*/, const double* /*b*/, double* /*c*/, int /*n*/) {
    // TODO: swap the two inner loops. Why does this help?
}

void matmul_blocked(const double* /*a*/, const double* /*b*/, double* /*c*/, int /*n*/) {
    // TODO: tile all three loops (try block sizes 32, 64, 128)
}

static double time_kernel(Kernel k, int n) {
    std::mt19937 gen(1);
    std::uniform_real_distribution<double> u(-1, 1);
    std::vector<double> a(n * n), b(n * n), c(n * n, 0.0);
    for (auto& x : a) x = u(gen);
    for (auto& x : b) x = u(gen);
    auto t0 = std::chrono::steady_clock::now();
    k(a.data(), b.data(), c.data(), n);
    auto t1 = std::chrono::steady_clock::now();
    volatile double sink = c[n / 2];  // keep the optimiser honest
    (void)sink;
    return std::chrono::duration<double>(t1 - t0).count();
}

int main() {
    struct {
        const char* name;
        Kernel k;
    } kernels[] = {{"ijk", matmul_ijk}, {"ikj", matmul_ikj}, {"blocked", matmul_blocked}};
    std::printf("%-8s %6s %10s %10s\n", "kernel", "n", "seconds", "GFLOP/s");
    for (int n : {256, 512, 1024}) {
        for (auto& [name, k] : kernels) {
            double s = time_kernel(k, n);
            std::printf("%-8s %6d %10.4f %10.2f\n", name, n, s, 2.0 * n * n * n / s / 1e9);
        }
    }
}

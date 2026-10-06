// Order-book latency benchmark. Milestone 2.
//
// Generates a realistic-ish random message stream (adds clustered near the touch, many cancels,
// occasional marketable orders), replays it, and reports per-operation latency percentiles.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <random>
#include <vector>

#include "order_book.hpp"

using namespace ob;

int main() {
    constexpr int kOps = 1'000'000;
    std::mt19937_64 rng(1);
    OrderBook book;
    std::vector<OrderId> live;
    live.reserve(kOps);
    std::vector<std::uint32_t> ns;
    ns.reserve(kOps);
    OrderId next = 1;

    for (int i = 0; i < kOps; ++i) {
        int op = int(rng() % 100);
        auto t0 = std::chrono::steady_clock::now();
        if (op < 55 || live.empty()) {
            Side s = (rng() & 1) ? Side::Buy : Side::Sell;
            Price px = 10'000 + (s == Side::Buy ? -1 : 1) * Price(1 + rng() % 30);
            book.add_limit(next, s, px, Qty(1 + rng() % 100));
            live.push_back(next++);
        } else if (op < 95) {
            std::size_t k = rng() % live.size();
            book.cancel(live[k]);
            live[k] = live.back();
            live.pop_back();
        } else {
            book.add_market(next++, (rng() & 1) ? Side::Buy : Side::Sell, Qty(1 + rng() % 200));
        }
        auto t1 = std::chrono::steady_clock::now();
        ns.push_back(std::uint32_t(std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count()));
    }

    std::sort(ns.begin(), ns.end());
    auto pct = [&](double p) { return ns[std::size_t(p * (ns.size() - 1))]; };
    std::printf("ops=%d  p50=%uns  p90=%uns  p99=%uns  p99.9=%uns  max=%uns\n", kOps, pct(0.5),
                pct(0.9), pct(0.99), pct(0.999), ns.back());
    // TODO(you): this naive per-op timing is misleading. steady_clock costs ~20ns per call on
    // Linux, and on some platforms (e.g. Windows/MinGW) its resolution is ~1us, so every op
    // reads as 0 or 1000ns. Fix it: measure the clock's overhead and resolution, then either time
    // batches of operations or read the TSC (__rdtsc) and calibrate it. Explain it in WRITEUP.md.
}

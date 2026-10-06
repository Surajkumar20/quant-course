// SPSC benchmark harness. Milestones 1, 4 and 5.
//
//  * throughput: producer pushes N ints as fast as possible, consumer pops them
//  * round-trip latency: thread A pushes a timestamp to q1, thread B echoes it back on q2,
//    A records (now - timestamp). Report p50/p99/p99.9.
//
// TODO(you): add a MutexQueue<T> baseline (std::mutex + std::deque) with the same interface
// and run every benchmark on both queues.
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <thread>

#include "spsc_queue.hpp"

int main() {
    constexpr std::uint64_t kN = 50'000'000;
    lf::SpscQueue<std::uint64_t, 4096> q;

    auto t0 = std::chrono::steady_clock::now();
    std::thread producer([&] {
        for (std::uint64_t i = 0; i < kN; ++i)
            while (!q.try_push(i)) {
            }
    });
    std::uint64_t sum = 0, got = 0;
    while (got < kN)
        if (auto v = q.try_pop()) {
            sum += *v;
            ++got;
        }
    producer.join();
    double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    std::printf("throughput: %.1f M msgs/s (checksum %llu)\n", kN / s / 1e6, (unsigned long long)sum);

    // TODO(you): round-trip latency benchmark with two queues.
}

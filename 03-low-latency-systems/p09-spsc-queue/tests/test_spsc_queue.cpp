#include <gtest/gtest.h>

#include <atomic>
#include <cstdint>
#include <memory>
#include <string>
#include <thread>

#include "spsc_queue.hpp"

using lf::SpscQueue;

TEST(Spsc, FifoSingleThread) {
    SpscQueue<int, 8> q;
    EXPECT_TRUE(q.empty());
    for (int i = 0; i < 5; ++i) EXPECT_TRUE(q.try_push(i));
    EXPECT_EQ(q.size(), 5u);
    for (int i = 0; i < 5; ++i) {
        auto v = q.try_pop();
        ASSERT_TRUE(v.has_value());
        EXPECT_EQ(*v, i);
    }
    EXPECT_FALSE(q.try_pop().has_value());
}

TEST(Spsc, HoldsExactlyCapacity) {
    SpscQueue<int, 4> q;
    EXPECT_EQ(q.capacity(), 4u);
    for (int i = 0; i < 4; ++i) EXPECT_TRUE(q.try_push(i));
    EXPECT_FALSE(q.try_push(99));
    EXPECT_EQ(q.size(), 4u);
    EXPECT_EQ(*q.try_pop(), 0);
    EXPECT_TRUE(q.try_push(4));
    EXPECT_FALSE(q.try_push(5));
}

TEST(Spsc, WrapsAroundManyTimes) {
    SpscQueue<std::uint64_t, 4> q;
    std::uint64_t next_in = 0, next_out = 0;
    for (int round = 0; round < 10000; ++round) {
        int n = 1 + round % 4;
        for (int i = 0; i < n; ++i) ASSERT_TRUE(q.try_push(next_in++));
        for (int i = 0; i < n; ++i) ASSERT_EQ(*q.try_pop(), next_out++);
    }
    EXPECT_TRUE(q.empty());
}

TEST(Spsc, MoveOnlyType) {
    SpscQueue<std::unique_ptr<int>, 4> q;
    EXPECT_TRUE(q.try_push(std::make_unique<int>(7)));
    auto p = q.try_pop();
    ASSERT_TRUE(p.has_value());
    EXPECT_EQ(**p, 7);
}

TEST(Spsc, FailedPushDoesNotConsumeValue) {
    SpscQueue<std::unique_ptr<int>, 2> q;
    q.try_push(std::make_unique<int>(1));
    q.try_push(std::make_unique<int>(2));
    auto p = std::make_unique<int>(3);
    EXPECT_FALSE(q.try_push(std::move(p)));
    ASSERT_NE(p, nullptr);  // still ours
    EXPECT_EQ(*p, 3);
}

namespace {
struct NoDefault {
    explicit NoDefault(int x) : v(x) {}
    int v;
};
struct Counted {
    static inline std::atomic<int> live{0};
    Counted() { ++live; }
    Counted(const Counted&) { ++live; }
    Counted(Counted&&) noexcept { ++live; }
    ~Counted() { --live; }
};
}  // namespace

TEST(Spsc, NonDefaultConstructible) {
    SpscQueue<NoDefault, 4> q;
    EXPECT_TRUE(q.try_push(NoDefault{5}));
    EXPECT_EQ(q.try_pop()->v, 5);
}

TEST(Spsc, DestroysRemainingElements) {
    Counted::live = 0;
    {
        SpscQueue<Counted, 8> q;
        for (int i = 0; i < 5; ++i) q.try_push(Counted{});
        q.try_pop();
        EXPECT_EQ(Counted::live.load(), 4);
    }
    EXPECT_EQ(Counted::live.load(), 0);
}

TEST(Spsc, TwoThreadStress) {
    constexpr std::uint64_t kN = 2'000'000;
    SpscQueue<std::uint64_t, 1024> q;
    std::thread producer([&] {
        for (std::uint64_t i = 0; i < kN; ++i)
            while (!q.try_push(i)) std::this_thread::yield();
    });
    std::uint64_t expected = 0;
    bool in_order = true;
    while (expected < kN) {
        if (auto v = q.try_pop()) {
            if (*v != expected) in_order = false;
            ++expected;
        }
    }
    producer.join();
    EXPECT_TRUE(in_order);
    EXPECT_TRUE(q.empty());
}

TEST(Spsc, TwoThreadStressStrings) {
    constexpr int kN = 200'000;
    SpscQueue<std::string, 64> q;
    std::thread producer([&] {
        for (int i = 0; i < kN; ++i) {
            std::string s = "msg-" + std::to_string(i) + std::string(i % 50, 'x');  // some heap-allocated
            while (!q.try_push(std::move(s))) std::this_thread::yield();
        }
    });
    int got = 0;
    bool ok = true;
    while (got < kN) {
        if (auto v = q.try_pop()) {
            ok &= v->rfind("msg-" + std::to_string(got), 0) == 0 && v->size() >= 4 + std::size_t(got % 50);
            ++got;
        }
    }
    producer.join();
    EXPECT_TRUE(ok);
}

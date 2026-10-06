#include <gtest/gtest.h>

#include <cmath>
#include <numbers>
#include <stdexcept>

#include "pde.hpp"

using namespace pde;

namespace {
const Market kMkt{100.0, 0.05, 0.2};
}

TEST(Tridiagonal, SolvesKnownSystem) {
    // [2 -1 0; -1 2 -1; 0 -1 2] x = [1 0 1]  ->  x = [1 1 1]
    auto x = solve_tridiagonal({0, -1, -1}, {2, 2, 2}, {-1, -1, 0}, {1, 0, 1});
    ASSERT_EQ(x.size(), 3u);
    for (double v : x) EXPECT_NEAR(v, 1.0, 1e-12);
}

TEST(Tridiagonal, LargerRandomLikeSystem) {
    const std::size_t n = 100;
    std::vector<double> lo(n), d(n), up(n), x_true(n), rhs(n);
    for (std::size_t i = 0; i < n; ++i) {
        lo[i] = -1.0 - 0.01 * i;
        up[i] = -0.5;
        d[i] = 4.0 + std::sin(double(i));
        x_true[i] = std::cos(0.1 * i);
    }
    for (std::size_t i = 0; i < n; ++i) {
        rhs[i] = d[i] * x_true[i];
        if (i > 0) rhs[i] += lo[i] * x_true[i - 1];
        if (i + 1 < n) rhs[i] += up[i] * x_true[i + 1];
    }
    auto x = solve_tridiagonal(lo, d, up, rhs);
    for (std::size_t i = 0; i < n; ++i) EXPECT_NEAR(x[i], x_true[i], 1e-12);
}

TEST(Explicit, StableGridIsAccurate) {
    Grid g{100, 2000, 4.0};
    for (Kind k : {Kind::Call, Kind::Put})
        EXPECT_NEAR(price_explicit(kMkt, {100, 1, k}, g), bs_price(kMkt, 100, 1, k), 0.05);
}

TEST(Explicit, UnstableGridThrows) {
    EXPECT_THROW(price_explicit(kMkt, {100, 1, Kind::Call}, Grid{200, 100, 4.0}), std::domain_error);
    EXPECT_THROW(price_explicit(kMkt, {100, 1, Kind::Put, Exercise::American}, Grid{100, 2000, 4.0}),
                 std::invalid_argument);
}

TEST(CrankNicolson, EuropeanMatchesBS) {
    Grid g{400, 400, 4.0};
    for (Kind k : {Kind::Call, Kind::Put})
        for (double K : {80.0, 100.0, 120.0})
            EXPECT_NEAR(price_crank_nicolson(kMkt, {K, 1, k}, g), bs_price(kMkt, K, 1, k), 1e-2)
                << "K=" << K;
}

TEST(CrankNicolson, OffNodeSpotIsInterpolated) {
    Market m{101.3, 0.05, 0.2};
    EXPECT_NEAR(price_crank_nicolson(m, {100, 1, Kind::Call}, Grid{400, 400, 4.0}),
                bs_price(m, 100, 1, Kind::Call), 2e-2);
}

TEST(CrankNicolson, ConvergesWithRefinement) {
    double truth = bs_price(kMkt, 100, 1, Kind::Put);
    double e1 = std::abs(price_crank_nicolson(kMkt, {100, 1, Kind::Put}, Grid{50, 50, 4.0}) - truth);
    double e2 = std::abs(price_crank_nicolson(kMkt, {100, 1, Kind::Put}, Grid{200, 200, 4.0}) - truth);
    EXPECT_LT(e2, e1 / 4.0);
}

TEST(American, PutHasEarlyExercisePremium) {
    Grid g{400, 400, 4.0};
    double euro = price_crank_nicolson(kMkt, {100, 1, Kind::Put, Exercise::European}, g);
    double amer = price_crank_nicolson(kMkt, {100, 1, Kind::Put, Exercise::American}, g);
    EXPECT_GT(amer, euro + 0.4);
    EXPECT_NEAR(amer, 6.0896, 1e-2);
}

TEST(American, PutNeverBelowIntrinsic) {
    Market m{80.0, 0.05, 0.2};
    double amer = price_crank_nicolson(m, {100, 1, Kind::Put, Exercise::American}, Grid{400, 400, 4.0});
    EXPECT_GE(amer, 20.0 - 1e-9);
}

TEST(American, CallNoDividendEqualsEuropean) {
    Grid g{400, 400, 4.0};
    double euro = price_crank_nicolson(kMkt, {100, 1, Kind::Call, Exercise::European}, g);
    double amer = price_crank_nicolson(kMkt, {100, 1, Kind::Call, Exercise::American}, g);
    EXPECT_NEAR(amer, euro, 1e-6);
}

TEST(Greeks, MatchBlackScholes) {
    // closed-form BS delta/gamma for S=K=100, T=1, r=5%, vol=20%
    const double d1 = (0.05 + 0.02) / 0.2;
    const double pdf = std::exp(-0.5 * d1 * d1) / std::sqrt(2 * std::numbers::pi);
    const double call_delta = 0.5 * std::erfc(-d1 / std::sqrt(2.0));
    const double gamma = pdf / (100 * 0.2);
    Greeks c = price_with_greeks(kMkt, {100, 1, Kind::Call}, Grid{400, 400, 4.0});
    Greeks p = price_with_greeks(kMkt, {100, 1, Kind::Put}, Grid{400, 400, 4.0});
    EXPECT_NEAR(c.price, bs_price(kMkt, 100, 1, Kind::Call), 1e-2);
    EXPECT_NEAR(c.delta, call_delta, 2e-3);
    EXPECT_NEAR(p.delta, call_delta - 1.0, 2e-3);
    EXPECT_NEAR(c.gamma, gamma, 5e-4);
    EXPECT_NEAR(p.gamma, gamma, 5e-4);
}

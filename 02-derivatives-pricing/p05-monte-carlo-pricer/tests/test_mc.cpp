#include <gtest/gtest.h>

#include <cmath>

#include "mc.hpp"

using namespace mc;

namespace {
const Market kMkt{100.0, 0.05, 0.0, 0.2};

// Statistical assertion: |estimate - truth| <= k standard errors.
void expect_within(const Result& r, double truth, double k = 4.0) {
    EXPECT_GT(r.std_error, 0.0);
    EXPECT_LE(std::abs(r.price - truth), k * r.std_error)
        << "price " << r.price << " truth " << truth << " se " << r.std_error;
}
}  // namespace

TEST(BlackScholes, TextbookValues) {
    EXPECT_NEAR(bs_price(kMkt, 100, 1, Kind::Call), 10.450583572, 1e-6);
    EXPECT_NEAR(bs_price(kMkt, 100, 1, Kind::Put), 5.573526022, 1e-6);
    Market d{100, 0.1, 0.03, 0.25};
    double c = bs_price(d, 100, 0.5, Kind::Call), p = bs_price(d, 100, 0.5, Kind::Put);
    EXPECT_NEAR(c - p, 100 * std::exp(-0.015) - 100 * std::exp(-0.05), 1e-9);
}

TEST(European, PlainMatchesBS) {
    for (Kind k : {Kind::Call, Kind::Put}) {
        for (double K : {80.0, 100.0, 120.0}) {
            Result r = price_european(kMkt, K, 1.0, k, 200'000, 7);
            EXPECT_EQ(r.n_paths, 200'000u);
            expect_within(r, bs_price(kMkt, K, 1.0, k));
        }
    }
}

TEST(European, StdErrorShrinksLikeRootN) {
    Result a = price_european(kMkt, 100, 1, Kind::Call, 10'000, 1);
    Result b = price_european(kMkt, 100, 1, Kind::Call, 160'000, 1);
    EXPECT_NEAR(a.std_error / b.std_error, 4.0, 0.4);
}

TEST(European, ReproducibleWithSeed) {
    Result a = price_european(kMkt, 100, 1, Kind::Call, 1000, 99);
    Result b = price_european(kMkt, 100, 1, Kind::Call, 1000, 99);
    EXPECT_DOUBLE_EQ(a.price, b.price);
}

TEST(European, AntitheticReducesVarianceForCall) {
    Result plain = price_european(kMkt, 100, 1, Kind::Call, 100'000, 3, false);
    Result anti = price_european(kMkt, 100, 1, Kind::Call, 50'000, 3, true);  // same # normals
    expect_within(anti, bs_price(kMkt, 100, 1, Kind::Call));
    EXPECT_LT(anti.std_error, 0.8 * plain.std_error);
}

TEST(European, ControlVariate) {
    Result plain = price_european(kMkt, 90, 1, Kind::Call, 100'000, 5);
    Result cv = price_european_cv(kMkt, 90, 1, Kind::Call, 100'000, 5);
    expect_within(cv, bs_price(kMkt, 90, 1, Kind::Call));
    EXPECT_LT(cv.std_error, 0.5 * plain.std_error);
}

TEST(European, WithDividends) {
    Market d{100, 0.03, 0.02, 0.3};
    expect_within(price_european(d, 105, 2, Kind::Put, 200'000, 11), bs_price(d, 105, 2, Kind::Put));
}

TEST(Asian, GeometricClosedFormSanity) {
    // one monitoring date at T: geometric Asian == European
    EXPECT_NEAR(asian_geometric_closed_form(kMkt, 100, 1, Kind::Call, 1),
                bs_price(kMkt, 100, 1, Kind::Call), 1e-10);
    // averaging lowers effective vol -> cheaper than European
    EXPECT_LT(asian_geometric_closed_form(kMkt, 100, 1, Kind::Call, 12),
              bs_price(kMkt, 100, 1, Kind::Call));
}

TEST(Asian, GeometricMCMatchesClosedForm) {
    for (Kind k : {Kind::Call, Kind::Put}) {
        Result r = price_asian(kMkt, 100, 1, k, Average::Geometric, 12, 100'000, 21);
        expect_within(r, asian_geometric_closed_form(kMkt, 100, 1, k, 12));
    }
}

TEST(Asian, ArithmeticAboveGeometricAndCVWorks) {
    double geo = asian_geometric_closed_form(kMkt, 100, 1, Kind::Call, 12);
    Result plain = price_asian(kMkt, 100, 1, Kind::Call, Average::Arithmetic, 12, 100'000, 8);
    Result cv = price_asian(kMkt, 100, 1, Kind::Call, Average::Arithmetic, 12, 100'000, 8, true);
    EXPECT_GT(cv.price, geo);  // AM-GM
    EXPECT_LE(std::abs(plain.price - cv.price), 4 * plain.std_error);
    EXPECT_LT(cv.std_error, plain.std_error / 7.0);  // variance reduction > 50x
}

TEST(Barrier, Bounds) {
    double vanilla = bs_price(kMkt, 100, 1, Kind::Call);
    Result far = price_up_and_out_call(kMkt, 100, 1e6, 1, 50, 100'000, 4);
    expect_within(far, vanilla);
    Result r = price_up_and_out_call(kMkt, 100, 130, 1, 50, 100'000, 4);
    EXPECT_GT(r.price, 0.0);
    EXPECT_LT(r.price, vanilla);
    Result dead = price_up_and_out_call(kMkt, 100, 100, 1, 50, 1'000, 4);
    EXPECT_DOUBLE_EQ(dead.price, 0.0);
}

TEST(Barrier, MoreMonitoringMeansCheaper) {
    Result coarse = price_up_and_out_call(kMkt, 100, 125, 1, 4, 200'000, 6);
    Result fine = price_up_and_out_call(kMkt, 100, 125, 1, 250, 200'000, 6);
    EXPECT_GT(coarse.price - fine.price, 3 * std::hypot(coarse.std_error, fine.std_error));
}

TEST(Threads, MultiThreadedMatchesBS) {
    for (unsigned t : {1u, 2u, 4u}) {
        Result r = price_european_mt(kMkt, 100, 1, Kind::Call, 400'000, 17, t);
        EXPECT_EQ(r.n_paths, 400'000u);
        expect_within(r, bs_price(kMkt, 100, 1, Kind::Call));
    }
}

TEST(Threads, ReproducibleForFixedThreadCount) {
    Result a = price_european_mt(kMkt, 100, 1, Kind::Call, 100'000, 5, 4);
    Result b = price_european_mt(kMkt, 100, 1, Kind::Call, 100'000, 5, 4);
    EXPECT_DOUBLE_EQ(a.price, b.price);
}

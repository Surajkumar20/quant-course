#include <gtest/gtest.h>

#include <stdexcept>

#include "tvm.hpp"

TEST(Tvm, FutureValue) {
    EXPECT_NEAR(tvm::future_value(100, 0.05, 0), 100.0, 1e-12);
    EXPECT_NEAR(tvm::future_value(100, 0.05, 2), 110.25, 1e-12);
}

TEST(Tvm, PresentValueInvertsFutureValue) {
    for (double r : {0.0, 0.01, 0.07, 0.25})
        for (int n : {1, 5, 30})
            EXPECT_NEAR(tvm::present_value(tvm::future_value(123.0, r, n), r, n), 123.0, 1e-9);
}

TEST(Tvm, NpvTwoYearBond) { EXPECT_NEAR(tvm::npv(0.05, {0, 100, 100}), 185.9410430839, 1e-8); }

TEST(Tvm, IrrSimple) { EXPECT_NEAR(tvm::irr({-100, 110}), 0.10, 1e-8); }

TEST(Tvm, IrrAnnuity) {
    std::vector<double> cfs{-1000};
    cfs.insert(cfs.end(), 20, 100.0);
    double r = tvm::irr(cfs);
    EXPECT_NEAR(tvm::npv(r, cfs), 0.0, 1e-6);
    EXPECT_NEAR(r, 0.0775, 1e-4);
}

TEST(Tvm, IrrNoSignChangeThrows) {
    EXPECT_THROW(tvm::irr({100, 100, 100}), std::invalid_argument);
}

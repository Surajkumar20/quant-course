#pragma once

#include <vector>

namespace tvm {

// Value of `pv` after `n` periods compounding at `rate` per period.
double future_value(double pv, double rate, int n);

// Value today of `fv` received after `n` periods.
double present_value(double fv, double rate, int n);

// Net present value; cashflows[0] occurs today (t = 0).
double npv(double rate, const std::vector<double>& cashflows);

// Internal rate of return by bisection on [-0.99, 10].
// Throws std::invalid_argument if npv does not change sign on that interval.
double irr(const std::vector<double>& cashflows, double tol = 1e-10);

}  // namespace tvm

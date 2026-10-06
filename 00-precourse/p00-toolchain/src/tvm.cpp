#include "tvm.hpp"

#include <stdexcept>

namespace tvm {

double future_value(double /*pv*/, double /*rate*/, int /*n*/) {
    throw std::logic_error("not implemented");
}

double present_value(double /*fv*/, double /*rate*/, int /*n*/) {
    throw std::logic_error("not implemented");
}

double npv(double /*rate*/, const std::vector<double>& /*cashflows*/) {
    throw std::logic_error("not implemented");
}

double irr(const std::vector<double>& /*cashflows*/, double /*tol*/) {
    throw std::logic_error("not implemented");
}

}  // namespace tvm

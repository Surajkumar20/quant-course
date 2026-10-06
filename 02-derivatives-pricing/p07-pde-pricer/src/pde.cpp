#include "pde.hpp"

#include <stdexcept>

namespace pde {

namespace {
[[noreturn]] void todo() { throw std::logic_error("not implemented"); }
}  // namespace

double bs_price(const Market&, double, double, Kind) { todo(); }

std::vector<double> solve_tridiagonal(const std::vector<double>&, const std::vector<double>&,
                                      const std::vector<double>&, const std::vector<double>&) {
    todo();
}

double price_explicit(const Market&, const Option&, const Grid&) { todo(); }

double price_crank_nicolson(const Market&, const Option&, const Grid&) { todo(); }

Greeks price_with_greeks(const Market&, const Option&, const Grid&) { todo(); }

}  // namespace pde

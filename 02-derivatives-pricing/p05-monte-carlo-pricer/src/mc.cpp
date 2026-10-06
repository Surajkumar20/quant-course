#include "mc.hpp"

#include <stdexcept>

namespace mc {

namespace {
[[noreturn]] void todo() { throw std::logic_error("not implemented"); }
}  // namespace

double bs_price(const Market&, double, double, Kind) { todo(); }

Result price_european(const Market&, double, double, Kind, std::size_t, std::uint64_t, bool) {
    todo();
}

Result price_european_cv(const Market&, double, double, Kind, std::size_t, std::uint64_t) {
    todo();
}

Result price_asian(const Market&, double, double, Kind, Average, std::size_t, std::size_t,
                   std::uint64_t, bool) {
    todo();
}

double asian_geometric_closed_form(const Market&, double, double, Kind, std::size_t) { todo(); }

Result price_up_and_out_call(const Market&, double, double, double, std::size_t, std::size_t,
                             std::uint64_t) {
    todo();
}

Result price_european_mt(const Market&, double, double, Kind, std::size_t, std::uint64_t,
                         unsigned) {
    todo();
}

}  // namespace mc

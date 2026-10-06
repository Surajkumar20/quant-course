#include "order_book.hpp"

#include <stdexcept>

namespace ob {

namespace {
[[noreturn]] void todo() { throw std::logic_error("not implemented"); }
}  // namespace

// Your state goes here. (Using a pimpl keeps the header stable while you swap data structures
// in milestone 3. Feel free to drop it and put members in the header instead.)
struct OrderBook::Impl {};

OrderBook::OrderBook() : impl_(new Impl) {}
OrderBook::~OrderBook() { delete impl_; }

std::vector<Trade> OrderBook::add_limit(OrderId, Side, Price, Qty) { todo(); }
std::vector<Trade> OrderBook::add_market(OrderId, Side, Qty) { todo(); }
bool OrderBook::cancel(OrderId) { todo(); }
bool OrderBook::reduce(OrderId, Qty) { todo(); }
std::optional<Price> OrderBook::best_bid() const { todo(); }
std::optional<Price> OrderBook::best_ask() const { todo(); }
Qty OrderBook::volume_at(Side, Price) const { todo(); }
std::size_t OrderBook::order_count() const { todo(); }
std::vector<std::pair<Price, Qty>> OrderBook::depth(Side, std::size_t) const { todo(); }

}  // namespace ob

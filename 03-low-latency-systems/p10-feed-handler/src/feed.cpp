#include "feed.hpp"

#include <stdexcept>

namespace feed {

namespace {
[[noreturn]] void todo() { throw std::logic_error("not implemented"); }
}  // namespace

Parser::Parser(Handler& handler) : handler_(handler) {}

std::size_t Parser::feed(const std::uint8_t*, std::size_t) { todo(); }
std::size_t Parser::unknown_messages() const { todo(); }
std::size_t Parser::buffered_bytes() const { todo(); }

void BookBuilder::on_add(const AddOrder&) { todo(); }
void BookBuilder::on_executed(const OrderExecuted&) { todo(); }
void BookBuilder::on_cancel(const OrderCancel&) { todo(); }
void BookBuilder::on_delete(const OrderDelete&) { todo(); }
void BookBuilder::on_replace(const OrderReplace&) { todo(); }

std::optional<Level> BookBuilder::best_bid(std::string_view) const { todo(); }
std::optional<Level> BookBuilder::best_ask(std::string_view) const { todo(); }
std::uint64_t BookBuilder::volume_at(std::string_view, char, std::uint32_t) const { todo(); }
std::size_t BookBuilder::live_orders() const { todo(); }

}  // namespace feed

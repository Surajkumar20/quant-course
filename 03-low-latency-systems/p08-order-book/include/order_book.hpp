#pragma once

#include <cstddef>
#include <cstdint>
#include <optional>
#include <utility>
#include <vector>

namespace ob {

using OrderId = std::uint64_t;
using Price = std::int64_t;  // integer ticks
using Qty = std::uint32_t;

enum class Side : std::uint8_t { Buy, Sell };

struct Trade {
    OrderId taker;  // incoming (aggressive) order
    OrderId maker;  // resting (passive) order
    Price price;    // always the maker's price
    Qty qty;

    bool operator==(const Trade&) const = default;
};

class OrderBook {
public:
    OrderBook();
    ~OrderBook();
    OrderBook(const OrderBook&) = delete;
    OrderBook& operator=(const OrderBook&) = delete;

    // Match against the opposite side; rest any remainder. Returns trades in execution order.
    std::vector<Trade> add_limit(OrderId id, Side side, Price price, Qty qty);

    // Match against the opposite side; discard any remainder.
    std::vector<Trade> add_market(OrderId id, Side side, Qty qty);

    bool cancel(OrderId id);
    bool reduce(OrderId id, Qty new_qty);

    std::optional<Price> best_bid() const;
    std::optional<Price> best_ask() const;

    // Total resting quantity at one price level (0 if none).
    Qty volume_at(Side side, Price price) const;

    // Number of live resting orders.
    std::size_t order_count() const;

    // Up to `levels` aggregated (price, total qty) pairs, best first.
    std::vector<std::pair<Price, Qty>> depth(Side side, std::size_t levels) const;

private:
    // Add your data structures here. Hint: start with
    //   std::map<Price, std::list<RestingOrder>, ...> for each side
    //   std::unordered_map<OrderId, Locator> for O(1) cancel
    struct Impl;
    Impl* impl_;
};

}  // namespace ob

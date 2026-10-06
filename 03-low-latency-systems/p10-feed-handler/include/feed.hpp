#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

namespace feed {

// Decoded messages. See PROTOCOL.md. `symbol` is right-trimmed of padding spaces.
struct AddOrder {
    std::uint64_t timestamp;
    std::uint64_t order_id;
    char side;  // 'B' or 'S'
    std::uint32_t shares;
    std::string symbol;
    std::uint32_t price;
};
struct OrderExecuted {
    std::uint64_t timestamp;
    std::uint64_t order_id;
    std::uint32_t shares;
    std::uint64_t match_id;
};
struct OrderCancel {
    std::uint64_t timestamp;
    std::uint64_t order_id;
    std::uint32_t shares;
};
struct OrderDelete {
    std::uint64_t timestamp;
    std::uint64_t order_id;
};
struct OrderReplace {
    std::uint64_t timestamp;
    std::uint64_t old_order_id;
    std::uint64_t new_order_id;
    std::uint32_t shares;
    std::uint32_t price;
};

class Handler {
public:
    virtual ~Handler() = default;
    virtual void on_add(const AddOrder&) {}
    virtual void on_executed(const OrderExecuted&) {}
    virtual void on_cancel(const OrderCancel&) {}
    virtual void on_delete(const OrderDelete&) {}
    virtual void on_replace(const OrderReplace&) {}
};

// Streaming parser. Chunks passed to feed() may split messages at any byte.
class Parser {
public:
    explicit Parser(Handler& handler);

    // Consume `len` bytes. Returns the number of *known* messages dispatched during this call.
    std::size_t feed(const std::uint8_t* data, std::size_t len);

    std::size_t unknown_messages() const;  // skipped messages with an unrecognised type
    std::size_t buffered_bytes() const;    // bytes of an incomplete message held for the next call

private:
    Handler& handler_;
    // add your state (e.g. a small buffer for a straddling message)
};

struct Level {
    std::uint32_t price;
    std::uint64_t shares;
    bool operator==(const Level&) const = default;
};

// Rebuilds aggregated per-symbol books from the feed.
class BookBuilder : public Handler {
public:
    void on_add(const AddOrder&) override;
    void on_executed(const OrderExecuted&) override;
    void on_cancel(const OrderCancel&) override;
    void on_delete(const OrderDelete&) override;
    void on_replace(const OrderReplace&) override;

    std::optional<Level> best_bid(std::string_view symbol) const;
    std::optional<Level> best_ask(std::string_view symbol) const;
    std::uint64_t volume_at(std::string_view symbol, char side, std::uint32_t price) const;
    std::size_t live_orders() const;

private:
    // add your state
};

}  // namespace feed

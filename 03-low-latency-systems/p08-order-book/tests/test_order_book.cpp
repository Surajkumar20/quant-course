#include <gtest/gtest.h>

#include <algorithm>
#include <map>
#include <random>
#include <stdexcept>

#include "order_book.hpp"

using namespace ob;
using Trades = std::vector<Trade>;

TEST(Book, EmptyBook) {
    OrderBook b;
    EXPECT_FALSE(b.best_bid());
    EXPECT_FALSE(b.best_ask());
    EXPECT_EQ(b.order_count(), 0u);
    EXPECT_TRUE(b.add_market(1, Side::Buy, 10).empty());
}

TEST(Book, RestingOrdersAndTouch) {
    OrderBook b;
    EXPECT_TRUE(b.add_limit(1, Side::Buy, 99, 10).empty());
    EXPECT_TRUE(b.add_limit(2, Side::Buy, 100, 5).empty());
    EXPECT_TRUE(b.add_limit(3, Side::Sell, 102, 7).empty());
    EXPECT_TRUE(b.add_limit(4, Side::Sell, 101, 3).empty());
    EXPECT_EQ(*b.best_bid(), 100);
    EXPECT_EQ(*b.best_ask(), 101);
    EXPECT_EQ(b.order_count(), 4u);
    EXPECT_EQ(b.volume_at(Side::Buy, 99), 10u);
    EXPECT_EQ(b.volume_at(Side::Sell, 150), 0u);
}

TEST(Book, CrossingLimitTradesAtMakerPrice) {
    OrderBook b;
    b.add_limit(1, Side::Sell, 101, 10);
    Trades t = b.add_limit(2, Side::Buy, 105, 4);
    ASSERT_EQ(t.size(), 1u);
    EXPECT_EQ(t[0], (Trade{2, 1, 101, 4}));
    EXPECT_EQ(b.volume_at(Side::Sell, 101), 6u);
    EXPECT_FALSE(b.best_bid());  // fully filled taker does not rest
}

TEST(Book, PriceTimePriority) {
    OrderBook b;
    b.add_limit(1, Side::Sell, 101, 5);
    b.add_limit(2, Side::Sell, 100, 5);
    b.add_limit(3, Side::Sell, 100, 5);
    Trades t = b.add_limit(9, Side::Buy, 101, 12);
    ASSERT_EQ(t.size(), 3u);
    EXPECT_EQ(t[0], (Trade{9, 2, 100, 5}));  // best price, earliest
    EXPECT_EQ(t[1], (Trade{9, 3, 100, 5}));
    EXPECT_EQ(t[2], (Trade{9, 1, 101, 2}));
    EXPECT_EQ(b.volume_at(Side::Sell, 101), 3u);
}

TEST(Book, RemainderRests) {
    OrderBook b;
    b.add_limit(1, Side::Sell, 100, 5);
    Trades t = b.add_limit(2, Side::Buy, 100, 8);
    ASSERT_EQ(t.size(), 1u);
    EXPECT_EQ(*b.best_bid(), 100);
    EXPECT_EQ(b.volume_at(Side::Buy, 100), 3u);
    EXPECT_FALSE(b.best_ask());
}

TEST(Book, MarketOrderSweepsAndDiscards) {
    OrderBook b;
    b.add_limit(1, Side::Buy, 100, 5);
    b.add_limit(2, Side::Buy, 99, 5);
    Trades t = b.add_market(3, Side::Sell, 20);
    ASSERT_EQ(t.size(), 2u);
    EXPECT_EQ(t[0], (Trade{3, 1, 100, 5}));
    EXPECT_EQ(t[1], (Trade{3, 2, 99, 5}));
    EXPECT_EQ(b.order_count(), 0u);
    EXPECT_FALSE(b.best_ask());  // remainder discarded, not rested
}

TEST(Book, Cancel) {
    OrderBook b;
    b.add_limit(1, Side::Buy, 100, 5);
    b.add_limit(2, Side::Buy, 100, 5);
    EXPECT_TRUE(b.cancel(1));
    EXPECT_FALSE(b.cancel(1));
    EXPECT_FALSE(b.cancel(42));
    EXPECT_EQ(b.volume_at(Side::Buy, 100), 5u);
    EXPECT_TRUE(b.cancel(2));
    EXPECT_FALSE(b.best_bid());  // empty level must disappear
}

TEST(Book, CannotCancelFilledOrder) {
    OrderBook b;
    b.add_limit(1, Side::Sell, 100, 5);
    b.add_limit(2, Side::Buy, 100, 5);
    EXPECT_FALSE(b.cancel(1));
    EXPECT_FALSE(b.cancel(2));
}

TEST(Book, ReduceKeepsPriority) {
    OrderBook b;
    b.add_limit(1, Side::Sell, 100, 10);
    b.add_limit(2, Side::Sell, 100, 10);
    EXPECT_TRUE(b.reduce(1, 4));
    EXPECT_FALSE(b.reduce(1, 4));   // not a reduction
    EXPECT_FALSE(b.reduce(1, 50));
    EXPECT_FALSE(b.reduce(77, 1));
    Trades t = b.add_market(3, Side::Buy, 6);
    ASSERT_EQ(t.size(), 2u);
    EXPECT_EQ(t[0], (Trade{3, 1, 100, 4}));
    EXPECT_EQ(t[1], (Trade{3, 2, 100, 2}));
    EXPECT_TRUE(b.reduce(2, 0));  // == cancel
    EXPECT_EQ(b.order_count(), 0u);
}

TEST(Book, InvalidInputs) {
    OrderBook b;
    b.add_limit(1, Side::Buy, 100, 5);
    EXPECT_THROW(b.add_limit(1, Side::Sell, 200, 5), std::invalid_argument);
    EXPECT_THROW(b.add_limit(2, Side::Buy, 100, 0), std::invalid_argument);
    EXPECT_THROW(b.add_market(3, Side::Buy, 0), std::invalid_argument);
}

TEST(Book, IdReusableAfterFill) {
    OrderBook b;
    b.add_limit(1, Side::Sell, 100, 5);
    b.add_market(2, Side::Buy, 5);
    EXPECT_NO_THROW(b.add_limit(1, Side::Buy, 90, 1));
}

TEST(Book, Depth) {
    OrderBook b;
    b.add_limit(1, Side::Buy, 100, 5);
    b.add_limit(2, Side::Buy, 100, 7);
    b.add_limit(3, Side::Buy, 98, 1);
    b.add_limit(4, Side::Buy, 99, 2);
    auto d = b.depth(Side::Buy, 2);
    ASSERT_EQ(d.size(), 2u);
    EXPECT_EQ(d[0], (std::pair<Price, Qty>{100, 12}));
    EXPECT_EQ(d[1], (std::pair<Price, Qty>{99, 2}));
    EXPECT_EQ(b.depth(Side::Buy, 10).size(), 3u);
    EXPECT_TRUE(b.depth(Side::Sell, 5).empty());
}

// ---------------------------------------------------------------------------
// Randomised differential test against a brute-force reference book.
// ---------------------------------------------------------------------------
namespace {
struct RefOrder {
    OrderId id;
    Side side;
    Price price;
    Qty qty;
    std::uint64_t seq;
};

class RefBook {
public:
    Trades add(OrderId id, Side side, std::optional<Price> limit, Qty qty) {
        Trades out;
        while (qty > 0) {
            auto best = orders_.end();
            for (auto it = orders_.begin(); it != orders_.end(); ++it) {
                if (it->side == side) continue;
                if (limit && (side == Side::Buy ? it->price > *limit : it->price < *limit)) continue;
                if (best == orders_.end()) { best = it; continue; }
                bool better = side == Side::Buy ? it->price < best->price : it->price > best->price;
                if (better || (it->price == best->price && it->seq < best->seq)) best = it;
            }
            if (best == orders_.end()) break;
            Qty q = std::min(qty, best->qty);
            out.push_back({id, best->id, best->price, q});
            qty -= q;
            best->qty -= q;
            if (best->qty == 0) orders_.erase(best);
        }
        if (qty > 0 && limit) orders_.push_back({id, side, *limit, qty, seq_++});
        return out;
    }
    bool cancel(OrderId id) {
        auto it = find(id);
        if (it == orders_.end()) return false;
        orders_.erase(it);
        return true;
    }
    bool reduce(OrderId id, Qty q) {
        auto it = find(id);
        if (it == orders_.end() || q >= it->qty) return false;
        if (q == 0) orders_.erase(it); else it->qty = q;
        return true;
    }
    std::optional<Price> best(Side s) const {
        std::optional<Price> b;
        for (auto& o : orders_)
            if (o.side == s && (!b || (s == Side::Buy ? o.price > *b : o.price < *b))) b = o.price;
        return b;
    }
    Qty volume(Side s, Price p) const {
        Qty v = 0;
        for (auto& o : orders_) if (o.side == s && o.price == p) v += o.qty;
        return v;
    }
    std::size_t count() const { return orders_.size(); }
    bool live(OrderId id) { return find(id) != orders_.end(); }

private:
    std::vector<RefOrder>::iterator find(OrderId id) {
        return std::find_if(orders_.begin(), orders_.end(), [&](auto& o) { return o.id == id; });
    }
    std::vector<RefOrder> orders_;
    std::uint64_t seq_ = 0;
};
}  // namespace

TEST(Book, RandomisedAgainstReference) {
    std::mt19937_64 rng(2024);
    OrderBook b;
    RefBook ref;
    OrderId next = 1;
    std::vector<OrderId> ids;
    for (int step = 0; step < 20000; ++step) {
        int op = int(rng() % 10);
        Side side = (rng() & 1) ? Side::Buy : Side::Sell;
        Qty qty = Qty(1 + rng() % 20);
        if (op < 6) {
            Price px = 1000 + Price(rng() % 21) - 10;
            OrderId id = next++;
            ids.push_back(id);
            ASSERT_EQ(b.add_limit(id, side, px, qty), ref.add(id, side, px, qty)) << "step " << step;
        } else if (op < 7) {
            OrderId id = next++;
            ASSERT_EQ(b.add_market(id, side, qty), ref.add(id, side, std::nullopt, qty)) << "step " << step;
        } else if (op < 9 && !ids.empty()) {
            OrderId id = ids[rng() % ids.size()];
            ASSERT_EQ(b.cancel(id), ref.cancel(id)) << "step " << step;
        } else if (!ids.empty()) {
            OrderId id = ids[rng() % ids.size()];
            Qty q = Qty(rng() % 15);
            ASSERT_EQ(b.reduce(id, q), ref.reduce(id, q)) << "step " << step;
        }
        ASSERT_EQ(b.best_bid(), ref.best(Side::Buy)) << "step " << step;
        ASSERT_EQ(b.best_ask(), ref.best(Side::Sell)) << "step " << step;
        ASSERT_EQ(b.order_count(), ref.count()) << "step " << step;
        if (step % 50 == 0)
            for (Price p = 985; p <= 1015; ++p) {
                ASSERT_EQ(b.volume_at(Side::Buy, p), ref.volume(Side::Buy, p));
                ASSERT_EQ(b.volume_at(Side::Sell, p), ref.volume(Side::Sell, p));
            }
    }
}

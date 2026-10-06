#include <gtest/gtest.h>

#include <random>
#include <string>
#include <vector>

#include "feed.hpp"

using namespace feed;
using Bytes = std::vector<std::uint8_t>;

// ---------------------------------------------------------------------------
// Test-side encoder (big-endian). Writing your own encoder is fine, but don't copy this
// into your parser. Decoding is the exercise.
// ---------------------------------------------------------------------------
namespace {
struct Enc {
    Bytes payload;
    void u8(std::uint8_t v) { payload.push_back(v); }
    void u32(std::uint32_t v) { for (int s = 24; s >= 0; s -= 8) payload.push_back(std::uint8_t(v >> s)); }
    void u64(std::uint64_t v) { for (int s = 56; s >= 0; s -= 8) payload.push_back(std::uint8_t(v >> s)); }
    void sym(const std::string& s) { for (int i = 0; i < 8; ++i) payload.push_back(i < int(s.size()) ? s[i] : ' '); }
    void frame_into(Bytes& out) const {
        out.push_back(std::uint8_t(payload.size() >> 8));
        out.push_back(std::uint8_t(payload.size() & 0xff));
        out.insert(out.end(), payload.begin(), payload.end());
    }
};

void add(Bytes& out, std::uint64_t ts, std::uint64_t id, char side, std::uint32_t sh, const std::string& sym, std::uint32_t px) {
    Enc e; e.u8('A'); e.u64(ts); e.u64(id); e.u8(std::uint8_t(side)); e.u32(sh); e.sym(sym); e.u32(px); e.frame_into(out);
}
void exec(Bytes& out, std::uint64_t ts, std::uint64_t id, std::uint32_t sh, std::uint64_t match) {
    Enc e; e.u8('E'); e.u64(ts); e.u64(id); e.u32(sh); e.u64(match); e.frame_into(out);
}
void cancel(Bytes& out, std::uint64_t ts, std::uint64_t id, std::uint32_t sh) {
    Enc e; e.u8('X'); e.u64(ts); e.u64(id); e.u32(sh); e.frame_into(out);
}
void del(Bytes& out, std::uint64_t ts, std::uint64_t id) {
    Enc e; e.u8('D'); e.u64(ts); e.u64(id); e.frame_into(out);
}
void replace(Bytes& out, std::uint64_t ts, std::uint64_t old_id, std::uint64_t new_id, std::uint32_t sh, std::uint32_t px) {
    Enc e; e.u8('U'); e.u64(ts); e.u64(old_id); e.u64(new_id); e.u32(sh); e.u32(px); e.frame_into(out);
}
void unknown(Bytes& out, std::size_t extra) {
    Enc e; e.u8('Z'); e.u64(1); for (std::size_t i = 0; i < extra; ++i) e.u8(0xAB); e.frame_into(out);
}

struct Recorder : Handler {
    std::vector<AddOrder> adds;
    std::vector<OrderExecuted> execs;
    std::vector<OrderCancel> cancels;
    std::vector<OrderDelete> deletes;
    std::vector<OrderReplace> replaces;
    void on_add(const AddOrder& m) override { adds.push_back(m); }
    void on_executed(const OrderExecuted& m) override { execs.push_back(m); }
    void on_cancel(const OrderCancel& m) override { cancels.push_back(m); }
    void on_delete(const OrderDelete& m) override { deletes.push_back(m); }
    void on_replace(const OrderReplace& m) override { replaces.push_back(m); }
};

Bytes sample_stream() {
    Bytes b;
    add(b, 1000, 1, 'B', 100, "AAPL", 1'500'000);
    add(b, 1001, 2, 'S', 50, "AAPL", 1'501'000);
    unknown(b, 7);
    add(b, 1002, 3, 'B', 200, "MSFT", 4'000'000);
    exec(b, 1003, 1, 30, 777);
    cancel(b, 1004, 2, 10);
    replace(b, 1005, 3, 4, 150, 4'001'000);
    del(b, 1006, 2);
    return b;
}
}  // namespace

TEST(Parser, DecodesAllFields) {
    Recorder r;
    Parser p(r);
    Bytes b = sample_stream();
    EXPECT_EQ(p.feed(b.data(), b.size()), 7u);
    EXPECT_EQ(p.unknown_messages(), 1u);
    EXPECT_EQ(p.buffered_bytes(), 0u);

    ASSERT_EQ(r.adds.size(), 3u);
    EXPECT_EQ(r.adds[0].timestamp, 1000u);
    EXPECT_EQ(r.adds[0].order_id, 1u);
    EXPECT_EQ(r.adds[0].side, 'B');
    EXPECT_EQ(r.adds[0].shares, 100u);
    EXPECT_EQ(r.adds[0].symbol, "AAPL");
    EXPECT_EQ(r.adds[0].price, 1'500'000u);
    EXPECT_EQ(r.adds[2].symbol, "MSFT");

    ASSERT_EQ(r.execs.size(), 1u);
    EXPECT_EQ(r.execs[0].order_id, 1u);
    EXPECT_EQ(r.execs[0].shares, 30u);
    EXPECT_EQ(r.execs[0].match_id, 777u);

    ASSERT_EQ(r.cancels.size(), 1u);
    EXPECT_EQ(r.cancels[0].shares, 10u);

    ASSERT_EQ(r.replaces.size(), 1u);
    EXPECT_EQ(r.replaces[0].old_order_id, 3u);
    EXPECT_EQ(r.replaces[0].new_order_id, 4u);
    EXPECT_EQ(r.replaces[0].price, 4'001'000u);

    ASSERT_EQ(r.deletes.size(), 1u);
    EXPECT_EQ(r.deletes[0].timestamp, 1006u);
}

TEST(Parser, LargeValuesAreBigEndian) {
    Bytes b;
    add(b, 0x0102030405060708ULL, 0xFFFFFFFFFFFFFFFEULL, 'S', 0xDEADBEEF, "ABCDEFGH", 0x7FFFFFFF);
    Recorder r;
    Parser p(r);
    p.feed(b.data(), b.size());
    ASSERT_EQ(r.adds.size(), 1u);
    EXPECT_EQ(r.adds[0].timestamp, 0x0102030405060708ULL);
    EXPECT_EQ(r.adds[0].order_id, 0xFFFFFFFFFFFFFFFEULL);
    EXPECT_EQ(r.adds[0].shares, 0xDEADBEEFu);
    EXPECT_EQ(r.adds[0].symbol, "ABCDEFGH");
    EXPECT_EQ(r.adds[0].price, 0x7FFFFFFFu);
}

TEST(Parser, ByteAtATime) {
    Bytes b = sample_stream();
    Recorder r;
    Parser p(r);
    std::size_t total = 0;
    for (std::uint8_t byte : b) total += p.feed(&byte, 1);
    EXPECT_EQ(total, 7u);
    EXPECT_EQ(r.adds.size(), 3u);
    EXPECT_EQ(r.adds[1].price, 1'501'000u);
    EXPECT_EQ(p.unknown_messages(), 1u);
}

TEST(Parser, RandomChunks) {
    Bytes b;
    for (int rep = 0; rep < 200; ++rep) {
        Bytes s = sample_stream();
        b.insert(b.end(), s.begin(), s.end());
    }
    std::mt19937 rng(5);
    Recorder r;
    Parser p(r);
    std::size_t pos = 0, total = 0;
    while (pos < b.size()) {
        std::size_t n = std::min<std::size_t>(1 + rng() % 70, b.size() - pos);
        total += p.feed(b.data() + pos, n);
        pos += n;
    }
    EXPECT_EQ(total, 7u * 200);
    EXPECT_EQ(r.adds.size(), 600u);
    EXPECT_EQ(p.unknown_messages(), 200u);
    EXPECT_EQ(p.buffered_bytes(), 0u);
}

TEST(Parser, IncompleteTailIsBuffered) {
    Bytes b;
    add(b, 1, 1, 'B', 1, "X", 1);
    Recorder r;
    Parser p(r);
    EXPECT_EQ(p.feed(b.data(), b.size() - 5), 0u);
    EXPECT_EQ(p.buffered_bytes(), b.size() - 5);
    EXPECT_EQ(p.feed(b.data() + b.size() - 5, 5), 1u);
    EXPECT_EQ(p.buffered_bytes(), 0u);
}

// ---------------------------------------------------------------------------
// BookBuilder
// ---------------------------------------------------------------------------
namespace {
BookBuilder build(const Bytes& b) {
    BookBuilder book;
    Parser p(book);
    p.feed(b.data(), b.size());
    return book;
}
}  // namespace

TEST(Book, AddsAggregateIntoLevels) {
    Bytes b;
    add(b, 1, 1, 'B', 100, "AAPL", 1'500'000);
    add(b, 2, 2, 'B', 50, "AAPL", 1'500'000);
    add(b, 3, 3, 'B', 10, "AAPL", 1'499'900);
    add(b, 4, 4, 'S', 70, "AAPL", 1'500'100);
    add(b, 5, 5, 'S', 30, "MSFT", 4'000'000);
    BookBuilder book = build(b);
    EXPECT_EQ(book.best_bid("AAPL"), (Level{1'500'000, 150}));
    EXPECT_EQ(book.best_ask("AAPL"), (Level{1'500'100, 70}));
    EXPECT_EQ(book.volume_at("AAPL", 'B', 1'499'900), 10u);
    EXPECT_FALSE(book.best_bid("MSFT"));
    EXPECT_EQ(book.best_ask("MSFT"), (Level{4'000'000, 30}));
    EXPECT_FALSE(book.best_bid("NOPE"));
    EXPECT_EQ(book.live_orders(), 5u);
}

TEST(Book, ExecuteCancelDelete) {
    Bytes b;
    add(b, 1, 1, 'B', 100, "AAPL", 1'500'000);
    add(b, 2, 2, 'B', 50, "AAPL", 1'500'000);
    exec(b, 3, 1, 40, 9);       // 60 left on #1
    cancel(b, 4, 2, 50);        // #2 gone
    BookBuilder book = build(b);
    EXPECT_EQ(book.best_bid("AAPL"), (Level{1'500'000, 60}));
    EXPECT_EQ(book.live_orders(), 1u);

    del(b, 5, 1);
    BookBuilder book2 = build(b);
    EXPECT_FALSE(book2.best_bid("AAPL"));
    EXPECT_EQ(book2.live_orders(), 0u);
    EXPECT_EQ(book2.volume_at("AAPL", 'B', 1'500'000), 0u);
}

TEST(Book, ReplaceKeepsSideAndSymbol) {
    Bytes b;
    add(b, 1, 1, 'S', 100, "TSLA", 2'000'000);
    replace(b, 2, 1, 7, 40, 1'990'000);
    BookBuilder book = build(b);
    EXPECT_EQ(book.best_ask("TSLA"), (Level{1'990'000, 40}));
    EXPECT_EQ(book.volume_at("TSLA", 'S', 2'000'000), 0u);
    EXPECT_EQ(book.live_orders(), 1u);
    // the new id is live, the old one is not
    exec(b, 3, 7, 40, 1);
    EXPECT_FALSE(build(b).best_ask("TSLA"));
}

TEST(Book, BestLevelMovesWhenTopEmpties) {
    Bytes b;
    add(b, 1, 1, 'S', 10, "AAPL", 100);
    add(b, 2, 2, 'S', 20, "AAPL", 101);
    add(b, 3, 3, 'B', 5, "AAPL", 99);
    add(b, 4, 4, 'B', 6, "AAPL", 98);
    exec(b, 5, 1, 10, 1);
    del(b, 6, 3);
    BookBuilder book = build(b);
    EXPECT_EQ(book.best_ask("AAPL"), (Level{101, 20}));
    EXPECT_EQ(book.best_bid("AAPL"), (Level{98, 6}));
}

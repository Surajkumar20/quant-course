# p08: Limit Order Book & Matching Engine

**Time:** ~2 weeks · **Language:** C++20 · **Track weight:** QD ★★★ QT ★★ QR ★

> "Design an order book" is the most common systems question at trading firms.
> After this project you'll have built one, tested it against a brute-force reference, and benchmarked it.

## Reading
- Harris, *Trading and Exchanges*, ch. 4–6 (orders, market structure, order-driven markets).
- [6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/): hashing, balanced BSTs, heaps. Which one fits each part of a book?
- [6.172](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/) L1–2 (Bentley rules), L11 (storage allocation), L14 (caching).

## Semantics (the tests enforce these)
- Prices are integer **ticks** (`int64_t`). Never use floating point for prices in a matching engine.
- **Price-time priority:** better price first; at the same price, earlier order first.
- An incoming order that crosses trades at the **resting (maker) order's price**.
- `add_limit` matches as much as possible, and any remainder **rests** on the book.
- `add_market` matches as much as possible, and the remainder is **discarded** (it never rests).
- `cancel(id)` removes a resting order. It returns `false` if the id is unknown or already fully filled.
- `reduce(id, new_qty)` lowers a resting order's quantity and **keeps its priority**. `new_qty == 0` behaves like cancel. Returns `false` if the id is unknown or `new_qty >=` the current quantity.
- Throws `std::invalid_argument` for a duplicate live order id or a zero quantity.

## What you'll build
[`include/order_book.hpp`](include/order_book.hpp) / [`src/order_book.cpp`](src/order_book.cpp). You choose the internal data structures; the header only fixes the public API.
Start simple: `std::map<Price, std::list<Order>>` per side plus `std::unordered_map<OrderId, iterator>`.

## Milestones
1. Make the tests pass with the simple design. The **randomised test** checks your book against a brute-force reference over 20,000 random operations.
2. Fill in [`bench/bench_book.cpp`](bench/bench_book.cpp): replay 1M random add/cancel/market operations and report **ns/op at p50/p99/p99.9**.
3. Optimise, measuring each step:
   - replace `std::list` with an intrusive list or index-based free list (no allocation per order)
   - replace `std::map` with a flat array of price levels indexed by `price - base` (prices cluster near the touch)
   - pre-size the hash map, or replace it with a flat vector indexed by order id if ids are dense
4. Write up a table of design → p50/p99. Explain each improvement with cache behaviour or allocation counts.

## Explain it in an interview
- Walk through the data structures and the complexity of add, cancel, match and best bid/ask.
- Why is cancel the most frequent operation on real exchanges, and how does that shape your design?
- Why is `std::map` a poor choice at the latency frontier even though it's O(log n)?
- How would you make this safe for multiple threads? Why do most real engines **avoid** that and run single-threaded per instrument?
- What's an iceberg order? A stop order? How would you add them?

## Stretch
- Order types: IOC, FOK, post-only, iceberg.
- Self-trade prevention.
- Feed it from your p10 feed handler and from your p09 queue (a matching thread fed by a network thread).

# p10: Binary Market-Data Feed Handler

**Time:** ~2 weeks · **Language:** C++20 · **Track weight:** QD ★★★ QR ★ QT ★

> Exchanges publish every order event as a binary stream, and firms rebuild the full order book from it, for
> thousands of symbols, at millions of messages per second. If you fall behind, you're trading on stale data.

## Reading
- [`PROTOCOL.md`](PROTOCOL.md): the wire format you'll parse. It's a subset in the style of NASDAQ ITCH 5.0.
- [6.172](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/) L10 (measurement & timing), L14 (caching), L3 (bit hacks, for byte-swapping).
- Harris, *Trading and Exchanges*, ch. 6 (order-driven markets) and the ITCH 5.0 specification.

## What you'll build
[`include/feed.hpp`](include/feed.hpp) / [`src/feed.cpp`](src/feed.cpp):
- `Parser`: a **streaming** decoder. `feed()` receives arbitrary byte chunks, which can split a message anywhere (even inside the 2-byte length). Complete messages go to a `Handler`, and unknown types are counted and skipped.
- `BookBuilder` (a `Handler`): keeps **aggregated price levels per symbol** (price → total shares) plus an order map (id → symbol, side, price, shares), and answers best bid/ask and volume-at-price queries.

[`tools/gen_feed.py`](tools/gen_feed.py) (provided) writes a realistic binary feed file of any size for benchmarking.

## Milestones
1. Parse every message type with correct big-endian decoding. Write your own byte-swap first, then compare it with `__builtin_bswap64` / `std::byteswap` (C++23).
2. Handle chunk boundaries. The tests feed the same stream byte by byte and in random chunk sizes.
3. `BookBuilder` passes its tests.
4. Generate a 10M-message file and measure **messages/second** end to end, reading the file into memory first so you aren't measuring disk.
5. Optimise and measure:
   - zero-copy: decode straight from the input buffer when a whole message is present, and copy only the straddling tail
   - replace virtual dispatch with templates/CRTP. Did it matter? Show the numbers.
   - symbol → integer id interning; flat arrays instead of `std::unordered_map<std::string, ...>`
6. **Integrate:** run the parser on one thread and the book builder on another, connected by your p09 queue. Measure again.

## Explain it in an interview
- Why big-endian on the wire? How do you byte-swap cheaply?
- Why is `reinterpret_cast<const Msg*>(buf)` on a packed struct risky (alignment, strict aliasing)? What's the safe alternative (`std::memcpy`/`std::bit_cast`)?
- A sequence gap: you missed a UDP packet. What do you do? (Look up how retransmission/snapshot recovery works.)
- How would you get the latency from wire to book under 1 µs? (Kernel bypass, busy-polling, core pinning, no allocation.)

## Stretch
- Parse a real ITCH 5.0 sample file (NASDAQ publishes samples on their FTP) and reconstruct the book for one symbol.
- Add a `MoldUDP64`-style packet layer with sequence numbers and gap detection.

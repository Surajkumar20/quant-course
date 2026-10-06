# p09: Lock-Free Single-Producer / Single-Consumer Queue

**Time:** ~2 weeks · **Language:** C++20 · **Track weight:** QD ★★★ QR ★ QT ★

> Trading systems are pipelines: a network thread decodes packets, a strategy thread decides, and an order thread sends.
> The queues between them must never take a lock and never allocate. This is the most important data structure on that path.

## Reading
- [6.172](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/) L6 (multicore), L7 (races & parallelism), L16 (nondeterministic parallel programming), L17 (**synchronization without locks**).
- [6.004](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/): the memory hierarchy and caches.
- Anthony Williams, *C++ Concurrency in Action*, ch. 5 (memory model & atomics) and ch. 7 (lock-free data structures).
- Preshing on Programming: "Acquire and Release Semantics", "Memory Barriers Are Like Source Control Operations" (blog posts).

## What you'll build
[`include/spsc_queue.hpp`](include/spsc_queue.hpp): a bounded ring buffer, `SpscQueue<T, Capacity>`.
- `try_push` returns `false` when full, and `try_pop` returns `std::nullopt` when empty. Neither blocks.
- It holds exactly `Capacity` elements (`Capacity` is a power of two).
- It works with **move-only** types (e.g. `std::unique_ptr`) and types that aren't default-constructible.
- There's exactly one producer thread and one consumer thread. No mutexes.

## Milestones
1. Write a `std::mutex` + `std::deque` version first (in `bench/`) as your baseline.
2. Implement the lock-free version with `std::atomic<size_t>` head/tail and **acquire/release** ordering. Write a comment justifying every `memory_order` you use.
3. Make the tests pass, then run them **under ThreadSanitizer** (`-fsanitize=thread`, Linux/macOS) with zero reports.
4. Benchmark ([`bench/bench_spsc.cpp`](bench/bench_spsc.cpp)): throughput (msgs/sec) and **round-trip latency** (ping-pong between two queues), comparing mutex against lock-free.
5. Optimise and measure each step:
   - put head and tail on **separate cache lines** (`alignas(std::hardware_destructive_interference_size)` or 64), which removes false sharing
   - **cache** the other side's index locally so you only read the shared atomic when the cached value says full/empty
   - pin threads to cores (`pthread_setaffinity_np` / `SetThreadAffinityMask`)

## Explain it in an interview
- Why is `memory_order_seq_cst` correct but slower? What exactly does acquire/release guarantee here?
- What is false sharing? How did you detect it and how much did fixing it buy you?
- Why a power-of-two capacity?
- Why does SPSC not need compare-and-swap, while MPMC does? What is the ABA problem?
- What happens if the consumer is slower than the producer for a long time? What should a trading system do then?

## Stretch
- A `try_push`/`try_pop` batch API (amortise the atomics).
- A seqlock for one-writer/many-reader market-data snapshots.
- An MPSC queue (Vyukov's intrusive design). Explain why it is not linearisable in the obvious way.

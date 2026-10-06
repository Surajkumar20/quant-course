#pragma once

#include <cstddef>
#include <optional>
#include <stdexcept>
#include <type_traits>

namespace lf {

// Bounded lock-free single-producer / single-consumer queue.
//
//  * try_push may only be called from ONE producer thread.
//  * try_pop  may only be called from ONE consumer thread.
//  * Holds exactly Capacity elements.
//  * Must support move-only and non-default-constructible T.
template <typename T, std::size_t Capacity>
class SpscQueue {
    static_assert(Capacity >= 2 && (Capacity & (Capacity - 1)) == 0, "Capacity must be a power of two");

public:
    SpscQueue() = default;
    ~SpscQueue() = default;  // must destroy any elements still in the queue
    SpscQueue(const SpscQueue&) = delete;
    SpscQueue& operator=(const SpscQueue&) = delete;

    // Returns false (and leaves `value` untouched) if the queue is full.
    bool try_push(const T& /*value*/) { throw std::logic_error("not implemented"); }
    bool try_push(T&& /*value*/) { throw std::logic_error("not implemented"); }

    // Returns std::nullopt if the queue is empty.
    std::optional<T> try_pop() { throw std::logic_error("not implemented"); }

    // Approximate when called concurrently; exact when the queue is quiescent.
    std::size_t size() const { throw std::logic_error("not implemented"); }
    bool empty() const { return size() == 0; }
    static constexpr std::size_t capacity() { return Capacity; }

private:
    // Your members go here: the slots, plus head/tail atomics on separate cache lines.
};

}  // namespace lf

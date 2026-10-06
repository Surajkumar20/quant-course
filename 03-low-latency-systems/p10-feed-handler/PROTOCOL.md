# QCX-ITCH: wire protocol for p10

A deliberately small subset in the style of NASDAQ TotalView-ITCH 5.0. Once you've built this, read the
[real ITCH 5.0 spec](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf):
most of it will look familiar.

## Framing

The stream is a sequence of messages:

```
+----------------+----------------------------+
| length: u16 BE | payload: `length` bytes    |
+----------------+----------------------------+
```

`length` counts the payload only, not the 2 length bytes. Every payload starts with

| Offset | Size | Field | Notes |
|---|---|---|---|
| 0 | 1 | type | ASCII message type |
| 1 | 8 | timestamp | u64 BE, nanoseconds since midnight |

**All integers are big-endian (network byte order).** Prices are u32 in units of 1/10,000 (so `1234500` = $123.45).

A parser **must skip** messages with an unknown type, using `length`. Exchanges add message types over time, and a feed handler that crashes on one is broken.

## Messages

### `A`: Add Order (payload 34 bytes)
| Off | Size | Field |
|---|---|---|
| 0 | 1 | `'A'` |
| 1 | 8 | timestamp |
| 9 | 8 | order_id (u64) |
| 17 | 1 | side: `'B'` buy, `'S'` sell |
| 18 | 4 | shares (u32) |
| 22 | 8 | symbol: ASCII, right-padded with spaces |
| 30 | 4 | price (u32, ×1e-4) |

### `E`: Order Executed (payload 29 bytes)
| Off | Size | Field |
|---|---|---|
| 0 | 1 | `'E'` |
| 1 | 8 | timestamp |
| 9 | 8 | order_id |
| 17 | 4 | executed shares |
| 21 | 8 | match_id (u64) |

Reduces the resting order by `executed shares`. The order is removed when it reaches 0.

### `X`: Order Cancel (payload 21 bytes)
| Off | Size | Field |
|---|---|---|
| 0 | 1 | `'X'` |
| 1 | 8 | timestamp |
| 9 | 8 | order_id |
| 17 | 4 | cancelled shares |

Partial cancel: reduces the order by `cancelled shares`. The order is removed when it reaches 0.

### `D`: Order Delete (payload 17 bytes)
| Off | Size | Field |
|---|---|---|
| 0 | 1 | `'D'` |
| 1 | 8 | timestamp |
| 9 | 8 | order_id |

### `U`: Order Replace (payload 33 bytes)
| Off | Size | Field |
|---|---|---|
| 0 | 1 | `'U'` |
| 1 | 8 | timestamp |
| 9 | 8 | original order_id |
| 17 | 8 | new order_id |
| 25 | 4 | shares |
| 29 | 4 | price |

Removes the original order and adds a new one with the **same side and symbol**. The new order goes to the back of the queue, losing its time priority.

#!/usr/bin/env python3
"""Generate a QCX-ITCH binary feed (see ../PROTOCOL.md) for benchmarking.

    python 03-low-latency-systems/p10-feed-handler/tools/gen_feed.py --messages 10000000 --out feed.bin

The message mix roughly follows real equity feeds: lots of adds and cancels/deletes, fewer
executions and replaces, and a small fraction of unknown types the parser must skip.
Also writes <out>.expected.txt with the final best bid/ask per symbol so you can check your
BookBuilder at scale.
"""
from __future__ import annotations

import argparse
import random
import struct

SYMBOLS = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "JPM", "XOM", "SPY"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--messages", type=int, default=1_000_000)
    ap.add_argument("--out", default="feed.bin")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    mid = {s: rng.randint(50, 500) * 10_000 for s in SYMBOLS}
    live: dict[int, list] = {}  # id -> [symbol, side, shares, price]
    live_ids: list[int] = []
    next_id = 1
    ts = 34_200_000_000_000  # 09:30 in ns

    def take_random_live() -> int | None:
        while live_ids:
            i = rng.randrange(len(live_ids))
            oid = live_ids[i]
            if oid in live:
                return oid
            live_ids[i] = live_ids[-1]
            live_ids.pop()
        return None

    out = bytearray()
    with open(args.out, "wb") as f:
        for n in range(args.messages):
            ts += rng.randint(50, 5_000)
            r = rng.random()
            oid = take_random_live() if r >= 0.45 else None
            if oid is None or r < 0.45:
                sym = rng.choice(SYMBOLS)
                side = rng.choice("BS")
                tick = 100
                off = rng.randint(1, 20) * tick
                price = mid[sym] - off if side == "B" else mid[sym] + off
                shares = rng.choice([100, 100, 100, 200, 300, 500, 1000]) + rng.randint(0, 99)
                payload = struct.pack(">cQQcI8sI", b"A", ts, next_id, side.encode(), shares,
                                      sym.ljust(8).encode(), price)
                live[next_id] = [sym, side, shares, price]
                live_ids.append(next_id)
                next_id += 1
            elif r < 0.80:
                payload = struct.pack(">cQQ", b"D", ts, oid)
                del live[oid]
            elif r < 0.88:
                o = live[oid]
                q = rng.randint(1, o[2])
                payload = struct.pack(">cQQI", b"X", ts, oid, q)
                o[2] -= q
                if o[2] == 0:
                    del live[oid]
            elif r < 0.96:
                o = live[oid]
                q = rng.randint(1, o[2])
                payload = struct.pack(">cQQIQ", b"E", ts, oid, q, n)
                o[2] -= q
                if o[2] == 0:
                    del live[oid]
            elif r < 0.995:
                o = live.pop(oid)
                new_price = o[3] + rng.choice([-100, 100])
                # keep the book uncrossed: bids stay below mid, asks above
                if o[1] == "B":
                    new_price = min(new_price, mid[o[0]] - 100)
                else:
                    new_price = max(new_price, mid[o[0]] + 100)
                new_shares = rng.randint(1, 1000)
                payload = struct.pack(">cQQQII", b"U", ts, oid, next_id, new_shares, new_price)
                live[next_id] = [o[0], o[1], new_shares, new_price]
                live_ids.append(next_id)
                next_id += 1
            else:
                payload = struct.pack(">cQ", b"S", ts) + bytes(rng.randint(0, 20))  # unknown type
            out += struct.pack(">H", len(payload)) + payload
            if len(out) > 1 << 20:
                f.write(out)
                out.clear()
        f.write(out)

    with open(args.out + ".expected.txt", "w") as f:
        for sym in SYMBOLS:
            bids = [o for o in live.values() if o[0] == sym and o[1] == "B"]
            asks = [o for o in live.values() if o[0] == sym and o[1] == "S"]
            def best(orders, pick):
                if not orders:
                    return "-"
                px = pick(o[3] for o in orders)
                return f"{px}x{sum(o[2] for o in orders if o[3] == px)}"
            f.write(f"{sym} bid {best(bids, max)} ask {best(asks, min)}\n")
    print(f"wrote {args.messages} messages to {args.out} ({len(live)} live orders at end)")


if __name__ == "__main__":
    main()

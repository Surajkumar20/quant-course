#!/usr/bin/env python3
"""Make-a-market game, in the style of trading-firm interviews.

    python 05-market-making/games/make_a_market.py
    python 05-market-making/games/make_a_market.py --game cards --informed 0.4

The hidden value is the sum of several random draws, revealed one at a time. Each round you
quote a two-sided market "bid @ ask" (e.g. `12 @ 14`). A counterparty then may trade 1 lot
against you:
  * with probability --informed it is INFORMED: it knows the final value and buys from you if
    your ask is below it, or sells to you if your bid is above it;
  * otherwise it is NOISE: it buys or sells at random, but only if your spread is <= its
    tolerance (noise traders won't pay a silly-wide spread).
After the last reveal, positions settle at the true value and you see your P&L, broken down
into spread earned vs. adverse selection lost.

Things to practise: centring your quote on the fair value, widening when uncertain, skewing
when you hold inventory, and updating immediately when information arrives.
"""
from __future__ import annotations

import argparse
import random

GAMES = {
    "dice": dict(desc="sum of 4 six-sided dice", draw=lambda r: r.randint(1, 6), n=4, mean=3.5),
    "cards": dict(desc="sum of 5 cards drawn (with replacement) from 1..13", draw=lambda r: r.randint(1, 13), n=5, mean=7.0),
}


def parse_quote(s: str) -> tuple[float, float] | None:
    s = s.replace(",", " ").replace("@", " ").replace("/", " ")
    parts = s.split()
    if len(parts) != 2:
        return None
    try:
        bid, ask = float(parts[0]), float(parts[1])
    except ValueError:
        return None
    return (bid, ask) if bid < ask else None


def play(game: str, informed: float, seed: int | None, rounds_per_reveal: int) -> None:
    r = random.Random(seed)
    g = GAMES[game]
    draws = [g["draw"](r) for _ in range(g["n"])]
    truth = sum(draws)
    pos, cash = 0, 0.0
    spread_pnl = adverse_pnl = 0.0
    print(f"\nHidden value: the {g['desc']}. You'll see one draw at a time.")
    print("Quote as 'bid ask' (e.g. '12 14'). 'q' to quit.\n")

    for k in range(g["n"] + 1):
        known = draws[:k]
        fair = sum(known) + (g["n"] - k) * g["mean"]
        if k:
            print(f"--- Reveal #{k}: {draws[k - 1]}   (revealed so far: {known})")
        if k == g["n"]:
            break
        for _ in range(rounds_per_reveal):
            raw = input(f"position {pos:+d} | your market> ").strip().lower()
            if raw in ("q", "quit"):
                return
            quote = parse_quote(raw)
            if quote is None:
                print("  format: bid ask with bid < ask")
                continue
            bid, ask = quote
            if r.random() < informed:
                if ask < truth:  # they buy from us: we sell below value
                    pos -= 1; cash += ask
                    print(f"  INFORMED buyer lifts your {ask:g} offer")
                    adverse_pnl += ask - truth
                elif bid > truth:  # they sell to us: we buy above value
                    pos += 1; cash -= bid
                    print(f"  INFORMED seller hits your {bid:g} bid")
                    adverse_pnl += truth - bid
                else:
                    print("  (no trade)")
            else:
                tolerance = 1.0 + 0.5 * (g["n"] - k)
                if ask - bid <= tolerance:
                    if r.random() < 0.5:  # noise buyer: we sell at our ask
                        pos -= 1; cash += ask
                        print(f"  noise buyer lifts {ask:g}")
                    else:  # noise seller: we buy at our bid
                        pos += 1; cash -= bid
                        print(f"  noise seller hits {bid:g}")
                    spread_pnl += (ask - bid) / 2
                else:
                    print(f"  (no trade, your spread {ask - bid:g} is too wide for noise traders)")

    pnl = cash + pos * truth
    print(f"\nTrue value: {truth}  (draws {draws})")
    print(f"Final position {pos:+d}, P&L {pnl:+.2f}")
    print(f"  ~spread captured from noise traders: {spread_pnl:+.2f}")
    print(f"  adverse selection vs informed:       {adverse_pnl:+.2f}")
    print("  (the rest is inventory P&L: noise trades marked to the true value)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", choices=GAMES, default="dice")
    ap.add_argument("--informed", type=float, default=0.3, help="probability a counterparty is informed")
    ap.add_argument("--rounds", type=int, default=2, help="quotes per reveal")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    play(a.game, a.informed, a.seed, a.rounds)

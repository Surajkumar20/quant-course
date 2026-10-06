#!/usr/bin/env python3
"""Timed mental-arithmetic drill in the style of trading-firm online assessments.

    python 00-precourse/drills/mental_math.py              # 8 minutes, mixed
    python 00-precourse/drills/mental_math.py --minutes 2 --kind mul
    python 00-precourse/drills/mental_math.py --history    # show past scores

Divisions and fractions are answered to 2 decimal places (within 0.01 counts as correct).
Scores are appended to drills/history.csv so you can watch them improve.
"""
from __future__ import annotations

import argparse
import csv
import random
import time
from datetime import datetime
from pathlib import Path

HISTORY = Path(__file__).with_name("history.csv")


def gen_add(r: random.Random):
    a, b = r.randint(100, 9999), r.randint(100, 9999)
    if r.random() < 0.5:
        return f"{a} + {b}", a + b
    a, b = max(a, b), min(a, b)
    return f"{a} - {b}", a - b


def gen_mul(r: random.Random):
    if r.random() < 0.6:
        a, b = r.randint(11, 99), r.randint(11, 99)
    else:
        a, b = r.randint(101, 999), r.randint(2, 9)
    return f"{a} × {b}", a * b


def gen_div(r: random.Random):
    b = r.randint(3, 19)
    a = r.randint(20, 999)
    return f"{a} ÷ {b}", round(a / b, 2)


def gen_frac(r: random.Random):
    d = r.randint(3, 16)
    n = r.randint(1, d - 1)
    return f"{n}/{d} as decimal", round(n / d, 2)


def gen_pct(r: random.Random):
    p = r.choice([5, 12.5, 15, 20, 25, 30, 35, 40, 60, 75, 120, 150])
    x = r.randint(2, 400) * r.choice([1, 2, 4, 5, 10])
    return f"{p}% of {x}", round(p * x / 100, 2)


KINDS = {"add": gen_add, "mul": gen_mul, "div": gen_div, "frac": gen_frac, "pct": gen_pct}


def correct(ans: str, expected: float) -> bool:
    try:
        return abs(float(ans.replace(",", "")) - expected) <= 0.0100001
    except ValueError:
        return False


def drill(minutes: float, kind: str, seed: int | None) -> None:
    r = random.Random(seed)
    gens = list(KINDS.values()) if kind == "mixed" else [KINDS[kind]]
    deadline = time.monotonic() + minutes * 60
    right = wrong = 0
    misses: list[str] = []
    print(f"{minutes:g} minutes, kind={kind}. Blank line skips. Ctrl-C quits.\n")
    try:
        while time.monotonic() < deadline:
            q, a = r.choice(gens)(r)
            left = int(deadline - time.monotonic())
            ans = input(f"[{left:3d}s | {right:3d}✓] {q} = ").strip()
            if time.monotonic() > deadline:
                print("time!")
                break
            if correct(ans, a):
                right += 1
            else:
                wrong += 1
                misses.append(f"{q} = {a:g} (you: {ans or '-'})")
    except (KeyboardInterrupt, EOFError):
        print()
    rate = right / minutes
    print(f"\nScore: {right} correct, {wrong} wrong  ({rate:.1f}/min; target 10/min)")
    for m in misses[-10:]:
        print("  missed:", m)
    new = not HISTORY.exists()
    with HISTORY.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["timestamp", "kind", "minutes", "right", "wrong"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), kind, minutes, right, wrong])


def history() -> None:
    if not HISTORY.exists():
        print("No history yet.")
        return
    with HISTORY.open() as f:
        for row in csv.DictReader(f):
            rate = int(row["right"]) / float(row["minutes"])
            print(f"{row['timestamp']}  {row['kind']:6s} {rate:5.1f}/min  " + "█" * int(rate * 2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--minutes", type=float, default=8)
    ap.add_argument("--kind", choices=["mixed", *KINDS], default="mixed")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--history", action="store_true")
    args = ap.parse_args()
    history() if args.history else drill(args.minutes, args.kind, args.seed)

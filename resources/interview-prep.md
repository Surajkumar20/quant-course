# Interview Prep

Run this alongside the projects from week 1. Answers are hidden in collapsible blocks.
**Say your reasoning out loud** before you open one. The interviewer cares more about how you got there than the number.

## What the interview loops look like (general shape, varies by firm and year)

| Stage | What it tests | How to prepare here |
|---|---|---|
| Online assessment | timed arithmetic (e.g. "80 in 8"), number sequences, a HackerRank coding task | `00-precourse/drills/mental_math.py`, daily DSA |
| Phone screen | probability & expected value, a coding question, "walk me through a project" | the puzzles below, your `WRITEUP.md`s |
| Superday / onsite | harder probability, market-making games, betting under uncertainty, system design (QD), research discussion (QR) | p15, mock interviews with your group |

Notes:
- Jane Street uses **OCaml** internally, but they **don't** expect you to know it. They hire strong programmers in any language and teach them OCaml. Python and C++ are fine.
- Quant dev roles at HFT firms (HRT, Jump, Citadel Securities, Optiver) go deep on **C++**: object lifetime, move semantics, templates, cache behaviour, lock-free code. That is what Phase 3 is for.
- Bank roles (Goldman Strats, JPM QR, MS) weight **derivatives pricing** and **stochastic calculus** more heavily. That is what Phase 2 is for.

---

## Probability & expected value

**1.** You roll a fair die until a 6 appears. What is the expected number of rolls?
<details><summary>Answer</summary>6. Geometric with p = 1/6, so E = 1/p.</details>

**2.** Expected number of fair coin flips to see HH? And HT?
<details><summary>Answer</summary>HH: 6. HT: 4. Set up states (start, "last flip was H") and solve the linear equations. HT is faster because a failed H doesn't send you back to the start.</details>

**3.** A family has two children and at least one is a boy. P(both boys)?
<details><summary>Answer</summary>1/3. Equally likely outcomes {BB, BG, GB}. Be ready for the "boy born on a Tuesday" variant (13/27).</details>

**4.** Roll a die and get paid its face value in dollars. You may reroll once, and must take the second roll if you do. What is the game worth?
<details><summary>Answer</summary>$4.25. Keep 4, 5 or 6; reroll 1–3. E = (4+5+6)/6 + (3/6)(3.5) = 2.5 + 1.75. Follow-up: with two rerolls it's worth 14/3 ≈ 4.67.</details>

**5.** Break a stick at two uniformly random points. P(the three pieces form a triangle)?
<details><summary>Answer</summary>1/4. No piece may exceed 1/2. Draw the unit square.</details>

**6.** X, Y iid Uniform(0,1). Find E[max(X,Y)], E[min(X,Y)] and E|X − Y|.
<details><summary>Answer</summary>2/3, 1/3, 1/3. In general the k-th order statistic of n uniforms has mean k/(n+1).</details>

**7.** Expected number of rolls of a die to see every face at least once?
<details><summary>Answer</summary>6(1 + 1/2 + … + 1/6) = 14.7. Coupon collector: a sum of geometrics.</details>

**8.** You have $1 and bet $1 on fair coin flips. You stop at $0 or $3. P(reach $3)?
<details><summary>Answer</summary>1/3. Your wealth is a martingale, so by optional stopping 1 = 3p. You build this in p01.</details>

**9.** 100 passengers board a plane with 100 seats. The first passenger sits in a random seat. Everyone after takes their own seat if it's free, otherwise a random free seat. P(the last passenger gets their own seat)?
<details><summary>Answer</summary>1/2. At the end the free seat is either seat 1 or seat 100, and the two are symmetric.</details>

**10.** Three random variables have the same pairwise correlation ρ. What is the smallest possible ρ?
<details><summary>Answer</summary>−1/2. The correlation matrix must be PSD, and its eigenvalues are 1+2ρ and 1−ρ (twice).</details>

**11.** A disease has 1% prevalence. A test has 99% sensitivity and 99% specificity. You test positive. P(you are sick)?
<details><summary>Answer</summary>1/2. Out of 10,000 people, 99 true positives and 99 false positives.</details>

**12.** Expected number of fixed points of a uniformly random permutation of n elements?
<details><summary>Answer</summary>1, for every n. Linearity of expectation over indicator variables.</details>

**13.** Shuffle a deck and turn cards over one at a time. Expected position of the first ace?
<details><summary>Answer</summary>53/5 = 10.6. The 4 aces split the 48 other cards into 5 gaps of equal expected size, 48/5. Add 1 for the ace itself.</details>

**14.** Standard Brownian motion starts at 0. P(it hits +1 before −2)?
<details><summary>Answer</summary>2/3. Optional stopping again: 0 = p·1 + (1−p)(−2).</details>

**15.** A coin lands heads with probability 0.6 and the bet pays even money. What fraction of your bankroll should you bet each time to maximise long-run growth?
<details><summary>Answer</summary>Kelly fraction f* = p − q = 0.2. Know the derivation (maximise E[log wealth]) and why practitioners bet fractional Kelly.</details>

**16.** Quick: an at-the-money call with S = 100, σ = 20% and T = 1 year (zero rates). Roughly what's it worth?
<details><summary>Answer</summary>≈ 0.4 · σ√T · S = 0.4 · 0.2 · 100 = $8 (exact BS ≈ 7.97). You check this in p04.</details>

**17.** You draw from Uniform(0,1) repeatedly until the running sum exceeds 1. Expected number of draws?
<details><summary>Answer</summary>e. P(N > n) = 1/n!, and summing gives e.</details>

**18.** You flip 100 fair coins. Approximately what is P(at least 60 heads)?
<details><summary>Answer</summary>≈ 2.8%. Mean 50, sd 5, and with continuity correction z = 1.9, so P ≈ 0.029. (The exact binomial tail is ≈ 2.84%.)</details>

---

## Market-making games

These are played live. The interviewer is your counterparty.

**Make me a market on the sum of two dice.** A good answer is something like "6.5 at 7.5" around the fair value of 7. Then the interviewer trades against you and reveals information ("one die is a 5"), and you **re-quote immediately** (new fair value 8.5).
What they're watching:
- your quote is centred on fair value, and the spread reflects your uncertainty
- you update fast and without anchoring on your old quote
- you manage inventory: if you're already long, skew your quote down
- you think about **adverse selection**: why is this person trading with me?

**Make a market on a quantity you don't know** (e.g. the number of hedge funds in NYC). Give a wide market, then tighten it as you reason it through. Never quote a single number.

**The betting game:** you start with $100, and the interviewer offers bets with stated odds. Decide size, not just direction. That makes it a Kelly problem.

Practice:
- Play these with your study group weekly, rotating who's the counterparty.
- p15 builds the quantitative backbone (inventory risk, optimal spread).

---

## Mental math

The target is **80 correct in 8 minutes** on mixed arithmetic: 2-digit × 2-digit, division to 2 decimals, fractions ↔ decimals, and percentages.
Use `python 00-precourse/drills/mental_math.py`. Ten minutes a day, every day, and track your score in `PROGRESS.md`.

Tricks to learn properly:
- squares up to 30², and (a+b)(a−b) for near-squares: 47 × 53 = 50² − 3² = 2491
- ×25 = ×100 / 4, ×125 = ×1000 / 8
- the fraction table 1/7 … 1/16 to 3 decimals
- percent change compounding: +10% then −10% = −1%

---

## Coding interviews

- **QD:** LeetCode medium/hard in **C++**. Know the STL cold. Expect "implement an LRU cache", "design an order book" (p08) and "implement a thread-safe queue" (p09).
- **QR/QT:** LeetCode easy/medium in Python, plus numpy/pandas fluency. Expect "simulate X and estimate Y" (p01).
- Practise on a plain editor with **no autocomplete**, since that's the interview environment.

## Talking about your projects

For each finished project, prepare a **two-minute story**: the problem, one hard bug, one number (accuracy, speed-up or Sharpe) and one thing you'd change.
Your `WRITEUP.md` files are the source material for this.

# Diagnostic

**Rules:** 2 hours, paper and pencil plus a bare editor (no autocomplete), no notes, no AI.
There are 20 questions worth 5 points each. You need **70** to start Phase 1.
Answers are at the bottom. Don't scroll until you're finished.

## A. Probability (30 pts)

1. Two fair dice are rolled. Given that the sum is 8, what is the probability that at least one die shows a 3?
2. X ~ Exponential(λ). Compute E[X], Var(X), and P(X > s + t | X > s).
3. You pick a uniformly random point in the unit square. What is the probability it lies within distance 1 of the origin?
4. X, Y are independent standard normals. What is the distribution of X + Y? Of X / Y? What is P(X > Y)?
5. A biased coin with unknown P(heads) = p has a Uniform(0,1) prior. You observe 3 heads in 3 flips. What is the posterior mean of p?
6. N ~ Poisson(λ). Each event is independently "marked" with probability q. What is the distribution of the number of marked events?

## B. Linear algebra & calculus (30 pts)

7. A = [[2, 1], [1, 2]]. Find its eigenvalues and eigenvectors, and compute A¹⁰ in closed form.
8. Show that for any real matrix A, AᵀA is positive semi-definite. When is it positive definite?
9. Derive the least-squares solution β̂ minimising ‖y − Xβ‖². State the condition for it to be unique.
10. Minimise f(w) = wᵀΣw subject to 1ᵀw = 1 (Σ symmetric positive definite). Give the answer in terms of Σ⁻¹.
11. Evaluate ∫₋∞^∞ e^(−x²/2) dx. Show the trick.
12. Taylor-expand log(1 + x) to third order and use it to estimate log(1.05).

## C. Programming (30 pts)

Write these in **Python** (13–15) and **C++** (16–18), without running them. Then type them in and test.

13. A function that returns the k most frequent elements of a list in O(n log k).
14. Simulate 10⁵ paths of a symmetric ±1 random walk of length 100 **using numpy only (no Python loops)** and estimate P(max of the walk ≥ 10).
15. Given a list of daily prices, return the maximum profit from one buy followed by one sell. O(n).
16. A class `RingBuffer<T, N>` with `push`, `pop` and `size`, backed by `std::array`.
17. Explain the output of a program that pushes 5 elements into a `std::vector<std::string>` and holds a `std::string&` to element 0 across the pushes. What is the bug?
18. Implement binary search on a sorted `std::vector<int>` returning the first index ≥ target.

## D. Finance intuition (10 pts)

19. A bond pays $100 in one year and $100 in two years. The rate is 5% (annual compounding). What is it worth today? If rates rise, does its price go up or down, and why?
20. Explain why a call option's price can never exceed the price of the underlying stock.

---
---
---

## Answers

<details><summary>Show answers</summary>

1. Outcomes summing to 8: (2,6),(3,5),(4,4),(5,3),(6,2), five in total. Those with a 3: two. **2/5**.
2. E = 1/λ, Var = 1/λ², and **P = P(X > t) = e^(−λt)** (memorylessness).
3. **π/4**.
4. X + Y ~ N(0, 2). X/Y ~ standard **Cauchy**. P(X > Y) = **1/2**.
5. Posterior is Beta(4, 1), so the mean is **4/5**.
6. **Poisson(λq)** (thinning).
7. λ = 3 with v = (1,1)/√2, and λ = 1 with v = (1,−1)/√2. A¹⁰ = ½[[3¹⁰+1, 3¹⁰−1],[3¹⁰−1, 3¹⁰+1]].
8. xᵀAᵀAx = ‖Ax‖² ≥ 0. It is PD iff A has full column rank.
9. β̂ = (XᵀX)⁻¹Xᵀy (normal equations). It is unique iff X has full column rank.
10. w* = Σ⁻¹1 / (1ᵀΣ⁻¹1). This is the minimum-variance portfolio, which you build in p13.
11. **√(2π)**. Square the integral and switch to polar coordinates.
12. x − x²/2 + x³/3. log(1.05) ≈ 0.05 − 0.00125 + 0.0000417 ≈ **0.04879**.
13. Count with a dict, then keep a min-heap of size k (`heapq.nlargest(k, counts.items(), key=...)`).
14. `steps = rng.choice([-1, 1], size=(100_000, 100)); paths = steps.cumsum(axis=1); (paths.max(axis=1) >= 10).mean()`, which gives ≈ 0.32. Check it with the reflection principle.
15. Track the running minimum. `best = max(best, p - min_so_far)`.
16. Keep head/tail indices mod N and a count, and decide what happens on push-when-full. You build a lock-free version in p09.
17. Reallocation invalidates references: the reference **dangles**, and reading through it is undefined behaviour.
18. `std::lower_bound`. Write it by hand with a half-open `[lo, hi)` interval.
19. 100/1.05 + 100/1.05² ≈ **$185.94**. Prices fall when rates rise, because future cash flows are discounted more.
20. The call pays max(S_T − K, 0) ≤ S_T. Owning the stock dominates owning the call, so by no-arbitrage C ≤ S.

</details>

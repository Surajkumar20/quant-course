# p01: Monte Carlo Probability Lab

**Time:** ~2 weeks · **Language:** Python (numpy) · **Track weight:** QR ★★★ QT ★★★ QD ★★

> "Simulate it, then prove it" is the most useful habit in quant interviews.
> Every probability answer you give should come with a sanity check you could code in five minutes.

## Reading
- [18.600](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/): all lectures. Do the problem sets, especially the ones on expectation, conditioning, and limit theorems.
- [6.0002](https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/) lectures 4–7: stochastic thinking, random walks, Monte Carlo, confidence intervals.
- [18.445](https://ocw.mit.edu/courses/18-445-introduction-to-stochastic-processes-spring-2015/) lectures on martingales & optional stopping. You need these for gambler's ruin.
- Blitzstein & Hwang ch. 1–7, 10.

## What you'll build
A module, [`mc_lab.py`](mc_lab.py), with pairs of functions: an **exact** answer derived on paper and a **simulated** answer. The tests check both.

| Function | Exact or simulated |
|---|---|
| `mc_mean_ci(samples, level)` | the CLT confidence interval you will reuse for the rest of the course |
| `estimate_pi(n, rng)` | simulated, returns estimate **and** standard error |
| `coupon_collector_expected(n)` / `coupon_collector_sim(...)` | exact / simulated |
| `gamblers_ruin_prob(start, target, p)` / `gamblers_ruin_sim(...)` | exact (biased coin too) / simulated |
| `walk_max_prob_exact(n_steps, level)` / `walk_max_prob_sim(...)` | reflection principle / **vectorised** simulation (no Python loops over paths) |
| `draws_until_sum_exceeds_one(n_trials, rng)` | simulated; the mean should be e |

## Milestones
1. **Derive on paper first.** Put your derivations (photos or LaTeX) in `derivations/`. Coupon collector, gambler's ruin for p ≠ ½, and the reflection principle are the core three.
2. Implement `mc_mean_ci` and `estimate_pi`. Plot the error against n on log-log axes and confirm the slope is −½.
3. Implement the exact/simulated pairs. The simulations must use the `rng` passed in, so that results are reproducible.
4. Make `walk_max_prob_sim` fully vectorised. Time it against a loop version and record the speed-up in your write-up.
5. **Coverage experiment:** run 1,000 independent experiments, build a 95% CI in each, and plot how often the CI contains the truth. It should be close to 95%. Explain any gap.

## Explain it in an interview
- Why is Monte Carlo error O(1/√n) regardless of dimension? Why does that matter for pricing?
- Derive the probability of ruin for a biased coin. What changes when p = ½?
- What is the reflection principle, and why does it give the factor of 2?
- You simulated something and got 0.317 ± 0.004, while the "known answer" is 0.33. What do you do?

## Stretch
- Expected number of flips until HTH vs HHT. Simulate it, then solve it exactly with a Markov chain (fundamental matrix).
- Implement importance sampling for P(Z > 5), Z ~ N(0,1), and show the variance reduction over naive MC.
- Penney's game: compute the best response to every 3-flip pattern.

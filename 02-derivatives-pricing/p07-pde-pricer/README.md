# p07: Finite-Difference PDE Pricer in C++

**Time:** ~3 weeks · **Language:** C++20 · **Track weight:** QD ★★★ QR ★★ QT ★

> Monte Carlo is general but slow, and it struggles with early exercise. Trees are intuitive but crude.
> Every bank's pricing library has a PDE engine at its core, because it gives prices *and* Greeks on a grid, quickly and to high accuracy.

## Reading
- [18.03SC](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/) as needed for ODE background.
- [18.085](https://ocw.mit.edu/courses/18-085-computational-science-and-engineering-i-fall-2008/): finite differences, tridiagonal systems.
- [18.086](https://ocw.mit.edu/courses/18-086-mathematical-methods-for-engineers-ii-spring-2006/): the heat equation, explicit vs implicit time-stepping, stability (von Neumann), Crank–Nicolson.
- [18.S096](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/) L19: deriving the Black–Scholes PDE.
- Wilmott, *Paul Wilmott Introduces Quantitative Finance*, the finite-difference chapters. Hull's numerical procedures chapter.

## The PDE
With τ = T − t (time to expiry), V(S, τ) satisfies

  ∂V/∂τ = ½σ²S² ∂²V/∂S² + rS ∂V/∂S − rV,  V(S, 0) = payoff(S)

on S ∈ [0, S_max] with S_max = `s_max_mult · K`. Use a uniform grid: N = `n_space` intervals in S and M = `n_time` steps in τ.

## What you'll build
[`include/pde.hpp`](include/pde.hpp) / [`src/pde.cpp`](src/pde.cpp):
- `solve_tridiagonal`: the Thomas algorithm, O(N)
- `price_explicit`: explicit Euler. It **must throw** when the step violates the stability bound (see header).
- `price_crank_nicolson`: European, and American via **PSOR** (projected successive over-relaxation)
- `price_with_greeks`: price, delta and gamma read straight off the final grid

## Milestones
1. Thomas algorithm, then the explicit scheme. Deliberately violate the stability bound **without** the throw and plot the blow-up.
2. Crank–Nicolson European. Plot log(error) against log(N) for N = M ∈ {50, 100, 200, 400, 800} and measure the convergence order.
3. You'll see ugly oscillations in gamma near the strike with large time steps. Add **Rannacher smoothing** (two or four implicit half-steps first) and show that they're gone.
4. American put via PSOR. Compare with your p04 binomial tree. Plot the early-exercise boundary.
5. Benchmark CN against your p05 MC and p04 tree at equal accuracy (1e-3). Report time-to-accuracy in a table.

## Explain it in an interview
- Explain the CFL-type stability condition for the explicit scheme. Why is CN unconditionally stable but still able to oscillate?
- Why transform to log-space (x = ln S)? What are the pros and cons?
- How do you get delta and gamma from a PDE grid? Why are they almost free?
- Boundary conditions at S = 0 and S = S_max: what do you impose, and how far out must S_max be?
- Why can't you just take max(V, payoff) after each CN step for an American option? (You can, roughly. Explain what PSOR does better.)

## Stretch
- Solve in log-space with a non-uniform grid concentrated around the strike.
- Barrier options (knock-out boundary = Dirichlet condition). Compare to p05.
- ADI scheme for a two-asset option or the Heston PDE.

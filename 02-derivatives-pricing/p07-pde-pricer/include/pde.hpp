#pragma once

#include <cstddef>
#include <vector>

namespace pde {

enum class Kind { Call, Put };
enum class Exercise { European, American };

struct Market {
    double spot;
    double rate;  // continuously compounded
    double vol;
};

struct Option {
    double strike;
    double expiry;
    Kind kind;
    Exercise exercise = Exercise::European;
};

struct Grid {
    std::size_t n_space = 400;  // N intervals in S: S_i = i * S_max / N, i = 0..N
    std::size_t n_time = 400;   // M steps in tau
    double s_max_mult = 4.0;    // S_max = s_max_mult * strike
};

struct Greeks {
    double price;
    double delta;
    double gamma;
};

// Black-Scholes closed form, for testing.
double bs_price(const Market& m, double strike, double expiry, Kind kind);

// Solve the tridiagonal system  lower[i] x[i-1] + diag[i] x[i] + upper[i] x[i+1] = rhs[i]
// (lower[0] and upper[n-1] are ignored) with the Thomas algorithm in O(n).
std::vector<double> solve_tridiagonal(const std::vector<double>& lower,
                                      const std::vector<double>& diag,
                                      const std::vector<double>& upper,
                                      const std::vector<double>& rhs);

// Explicit (forward Euler in tau) scheme, European only.
// Throws std::domain_error if vol^2 * N^2 * dtau > 1 (the stability bound), and
// std::invalid_argument for American options.
// The price at `spot` is linearly interpolated between grid nodes.
double price_explicit(const Market& m, const Option& o, const Grid& g);

// Crank-Nicolson. American exercise via PSOR (or another projected method).
double price_crank_nicolson(const Market& m, const Option& o, const Grid& g);

// Crank-Nicolson price plus delta and gamma from central differences on the final grid.
// Tests only use a spot that sits exactly on a grid node.
Greeks price_with_greeks(const Market& m, const Option& o, const Grid& g);

}  // namespace pde

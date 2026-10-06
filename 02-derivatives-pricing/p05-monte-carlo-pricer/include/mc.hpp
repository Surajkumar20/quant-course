#pragma once

#include <cstddef>
#include <cstdint>

namespace mc {

enum class Kind { Call, Put };
enum class Average { Arithmetic, Geometric };

struct Market {
    double spot;
    double rate;      // continuously compounded risk-free rate
    double div;       // continuous dividend yield
    double vol;       // annualised volatility
};

struct Result {
    double price;
    double std_error;
    std::size_t n_paths;
};

// Black-Scholes closed form (reference).
double bs_price(const Market& m, double strike, double expiry, Kind kind);

// Plain Monte Carlo on S_T. With antithetic = true, n_paths counts *pairs* (Z, -Z), each pair
// averaged into one sample, so std_error must be computed from the n_paths pair-averages.
Result price_european(const Market& m, double strike, double expiry, Kind kind,
                      std::size_t n_paths, std::uint64_t seed, bool antithetic = false);

// Control variate: S_T, with E[S_T] = S_0 exp((r - q) T). Estimate the coefficient from the sample.
Result price_european_cv(const Market& m, double strike, double expiry, Kind kind,
                         std::size_t n_paths, std::uint64_t seed);

// Discretely monitored Asian option, averaging S at t_i = i T / n_steps for i = 1..n_steps.
// If geometric_cv is true (only meaningful for Average::Arithmetic), use the geometric Asian
// payoff as a control variate with its closed-form expectation.
Result price_asian(const Market& m, double strike, double expiry, Kind kind, Average avg,
                   std::size_t n_steps, std::size_t n_paths, std::uint64_t seed,
                   bool geometric_cv = false);

// Closed form for the discretely monitored geometric-average Asian (same monitoring dates).
double asian_geometric_closed_form(const Market& m, double strike, double expiry, Kind kind,
                                   std::size_t n_steps);

// Up-and-out call, barrier checked at t_i = i T / n_steps for i = 1..n_steps. The option is
// knocked out if S(t_i) >= barrier at any monitoring date. If spot >= barrier, the price is 0.
Result price_up_and_out_call(const Market& m, double strike, double barrier, double expiry,
                             std::size_t n_steps, std::size_t n_paths, std::uint64_t seed);

// Same estimator as price_european (no antithetics), split across n_threads std::threads, each
// with its own independent RNG stream.
Result price_european_mt(const Market& m, double strike, double expiry, Kind kind,
                         std::size_t n_paths, std::uint64_t seed, unsigned n_threads);

}  // namespace mc

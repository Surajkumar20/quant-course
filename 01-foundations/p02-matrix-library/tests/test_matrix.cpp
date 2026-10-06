#include <gtest/gtest.h>

#include <cmath>
#include <random>
#include <stdexcept>

#include "matrix.hpp"

using la::Matrix;
using la::Vector;

namespace {

Matrix random_matrix(std::size_t r, std::size_t c, unsigned seed) {
    std::mt19937_64 gen(seed);
    std::normal_distribution<double> n(0.0, 1.0);
    Matrix m(r, c);
    for (std::size_t i = 0; i < r; ++i)
        for (std::size_t j = 0; j < c; ++j) m(i, j) = n(gen);
    return m;
}

double max_abs(const Vector& v) {
    double m = 0;
    for (double x : v) m = std::max(m, std::abs(x));
    return m;
}

}  // namespace

// ---------- basics ----------

TEST(Matrix, ConstructAndIndex) {
    Matrix m(2, 3, 1.5);
    EXPECT_EQ(m.rows(), 2u);
    EXPECT_EQ(m.cols(), 3u);
    EXPECT_DOUBLE_EQ(m(1, 2), 1.5);
    m(1, 2) = 7.0;
    EXPECT_DOUBLE_EQ(m(1, 2), 7.0);
}

TEST(Matrix, InitializerList) {
    Matrix m{{1, 2, 3}, {4, 5, 6}};
    EXPECT_EQ(m.rows(), 2u);
    EXPECT_EQ(m.cols(), 3u);
    EXPECT_DOUBLE_EQ(m(1, 0), 4.0);
    EXPECT_THROW((Matrix{{1, 2}, {3}}), std::invalid_argument);
}

TEST(Matrix, IdentityAndTranspose) {
    Matrix i3 = Matrix::identity(3);
    EXPECT_DOUBLE_EQ(i3(0, 0), 1.0);
    EXPECT_DOUBLE_EQ(i3(0, 1), 0.0);
    Matrix m{{1, 2, 3}, {4, 5, 6}};
    Matrix t = m.transpose();
    EXPECT_EQ(t.rows(), 3u);
    EXPECT_DOUBLE_EQ(t(2, 1), 6.0);
}

TEST(Matrix, Arithmetic) {
    Matrix a{{1, 2}, {3, 4}};
    Matrix b{{5, 6}, {7, 8}};
    EXPECT_TRUE(la::approx_equal(a * b, Matrix{{19, 22}, {43, 50}}));
    EXPECT_TRUE(la::approx_equal(a + b, Matrix{{6, 8}, {10, 12}}));
    EXPECT_TRUE(la::approx_equal(b - a, Matrix{{4, 4}, {4, 4}}));
    EXPECT_TRUE(la::approx_equal(2.0 * a, Matrix{{2, 4}, {6, 8}}));
    Vector y = a * Vector{1, 1};
    EXPECT_DOUBLE_EQ(y[0], 3.0);
    EXPECT_DOUBLE_EQ(y[1], 7.0);
}

TEST(Matrix, RectangularMultiply) {
    Matrix a{{1, 2, 3}};       // 1x3
    Matrix b{{1}, {1}, {1}};   // 3x1
    EXPECT_TRUE(la::approx_equal(a * b, Matrix{{6}}));
    EXPECT_EQ((b * a).rows(), 3u);
    EXPECT_EQ((b * a).cols(), 3u);
}

TEST(Matrix, DimensionMismatchThrows) {
    Matrix a(2, 3), b(2, 2);
    EXPECT_THROW(a * a, std::invalid_argument);
    EXPECT_THROW(a + b, std::invalid_argument);
    EXPECT_THROW((a * Vector{1, 2}), std::invalid_argument);
}

TEST(Matrix, ApproxEqualShapes) {
    EXPECT_FALSE(la::approx_equal(Matrix(2, 2), Matrix(2, 3)));
}

// ---------- LU ----------

TEST(LU, ReconstructsPA) {
    Matrix a{{0, 2, 1}, {1, 1, 1}, {2, 1, 0}};  // a(0,0) == 0 forces a pivot
    la::LU f = la::lu_decompose(a);
    const std::size_t n = 3;
    Matrix L = Matrix::identity(n), U(n, n);
    for (std::size_t i = 0; i < n; ++i)
        for (std::size_t j = 0; j < n; ++j) (j < i ? L(i, j) : U(i, j)) = f.lu(i, j);
    Matrix pa(n, n);
    for (std::size_t i = 0; i < n; ++i)
        for (std::size_t j = 0; j < n; ++j) pa(i, j) = a(f.perm[i], j);
    EXPECT_TRUE(la::approx_equal(L * U, pa, 1e-12));
}

TEST(LU, PartialPivotingPicksLargest) {
    Matrix a{{1e-20, 1}, {1, 1}};
    la::LU f = la::lu_decompose(a);
    EXPECT_EQ(f.perm[0], 1u);
    Vector x = la::solve(a, {1, 2});
    EXPECT_NEAR(x[0], 1.0, 1e-12);
    EXPECT_NEAR(x[1], 1.0, 1e-12);
}

TEST(LU, SingularThrows) {
    Matrix s{{1, 2}, {2, 4}};
    EXPECT_THROW(la::lu_decompose(s), std::domain_error);
    EXPECT_THROW(la::lu_decompose(Matrix(2, 3)), std::invalid_argument);
}

TEST(LU, Determinant) {
    EXPECT_NEAR(la::determinant(Matrix{{1, 2}, {3, 4}}), -2.0, 1e-12);
    EXPECT_NEAR(la::determinant(Matrix{{0, 1}, {1, 0}}), -1.0, 1e-12);
    EXPECT_NEAR(la::determinant(Matrix{{2, 0, 0}, {0, 3, 0}, {0, 0, 4}}), 24.0, 1e-12);
    EXPECT_DOUBLE_EQ(la::determinant(Matrix{{1, 2}, {2, 4}}), 0.0);
}

TEST(LU, SolveRandomLarge) {
    const std::size_t n = 60;
    Matrix a = random_matrix(n, n, 42);
    Vector b(n);
    for (std::size_t i = 0; i < n; ++i) b[i] = std::sin(double(i));
    la::LU f = la::lu_decompose(a);
    Vector x = la::solve(f, b);
    Vector r = a * x;
    for (std::size_t i = 0; i < n; ++i) r[i] -= b[i];
    EXPECT_LT(max_abs(r), 1e-9);
}

TEST(LU, Inverse) {
    Matrix a = random_matrix(8, 8, 7);
    EXPECT_TRUE(la::approx_equal(a * la::inverse(a), Matrix::identity(8), 1e-9));
}

// ---------- Cholesky ----------

TEST(Cholesky, KnownExample) {
    Matrix a{{4, 12, -16}, {12, 37, -43}, {-16, -43, 98}};
    Matrix l = la::cholesky(a);
    EXPECT_TRUE(la::approx_equal(l, Matrix{{2, 0, 0}, {6, 1, 0}, {-8, 5, 3}}, 1e-12));
}

TEST(Cholesky, RandomSPD) {
    Matrix b = random_matrix(10, 10, 3);
    Matrix a = b * b.transpose() + Matrix::identity(10);
    Matrix l = la::cholesky(a);
    EXPECT_TRUE(la::approx_equal(l * l.transpose(), a, 1e-9));
    for (std::size_t i = 0; i < 10; ++i)
        for (std::size_t j = i + 1; j < 10; ++j) EXPECT_DOUBLE_EQ(l(i, j), 0.0);
}

TEST(Cholesky, RejectsNonSPD) {
    EXPECT_THROW(la::cholesky(Matrix{{1, 2}, {2, 1}}), std::domain_error);   // indefinite
    EXPECT_THROW(la::cholesky(Matrix{{1, 2}, {0, 1}}), std::domain_error);   // not symmetric
}

// ---------- least squares ----------

TEST(LeastSquares, ExactLine) {
    // y = 2 + 3x, exactly
    Matrix a{{1, 0}, {1, 1}, {1, 2}, {1, 3}};
    Vector x = la::least_squares(a, {2, 5, 8, 11});
    EXPECT_NEAR(x[0], 2.0, 1e-10);
    EXPECT_NEAR(x[1], 3.0, 1e-10);
}

TEST(LeastSquares, NoisyMatchesNormalEquations) {
    Matrix a = random_matrix(50, 4, 11);
    Vector b(50);
    for (std::size_t i = 0; i < 50; ++i) b[i] = std::cos(double(i));
    Vector x = la::least_squares(a, b);
    // optimality condition: A^T (A x - b) = 0
    Vector r = a * x;
    for (std::size_t i = 0; i < 50; ++i) r[i] -= b[i];
    EXPECT_LT(max_abs(a.transpose() * r), 1e-9);
}

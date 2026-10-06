#pragma once

#include <cstddef>
#include <initializer_list>
#include <vector>

namespace la {

// Dense, row-major matrix of doubles.
class Matrix {
public:
    Matrix() = default;
    Matrix(std::size_t rows, std::size_t cols, double fill = 0.0);
    // Matrix m{{1, 2}, {3, 4}};  throws std::invalid_argument on ragged rows.
    Matrix(std::initializer_list<std::initializer_list<double>> rows);

    static Matrix identity(std::size_t n);

    std::size_t rows() const { return rows_; }
    std::size_t cols() const { return cols_; }

    double& operator()(std::size_t i, std::size_t j);
    double operator()(std::size_t i, std::size_t j) const;

    Matrix transpose() const;

private:
    std::size_t rows_ = 0;
    std::size_t cols_ = 0;
    std::vector<double> data_;  // element (i, j) lives at data_[i * cols_ + j]
};

using Vector = std::vector<double>;

// All binary ops throw std::invalid_argument on dimension mismatch.
Matrix operator+(const Matrix& a, const Matrix& b);
Matrix operator-(const Matrix& a, const Matrix& b);
Matrix operator*(const Matrix& a, const Matrix& b);
Matrix operator*(double s, const Matrix& a);
Vector operator*(const Matrix& a, const Vector& x);

// Max-abs elementwise comparison; false if shapes differ.
bool approx_equal(const Matrix& a, const Matrix& b, double tol = 1e-9);

// LU decomposition with partial pivoting: P A = L U.
//   lu   : L (strictly below the diagonal, unit diagonal implied) and U (on and above) packed together
//   perm : row i of P A is row perm[i] of A
//   sign : +1 or -1, the sign of the permutation (needed for the determinant)
// Throws std::invalid_argument if A is not square, std::domain_error if A is singular
// (a pivot with |pivot| < 1e-12).
struct LU {
    Matrix lu;
    std::vector<std::size_t> perm;
    int sign = 1;
};
LU lu_decompose(const Matrix& a);

Vector solve(const LU& f, const Vector& b);  // reuse a factorisation
Vector solve(const Matrix& a, const Vector& b);
double determinant(const Matrix& a);  // returns 0.0 for singular matrices (does not throw)
Matrix inverse(const Matrix& a);

// Lower-triangular L with A = L L^T. Throws std::domain_error if A is not symmetric positive-definite.
Matrix cholesky(const Matrix& a);

// argmin_x ||A x - b||_2 for a tall matrix A (rows >= cols) with full column rank.
Vector least_squares(const Matrix& a, const Vector& b);

}  // namespace la

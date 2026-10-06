#include "matrix.hpp"

#include <stdexcept>

namespace la {

namespace {
[[noreturn]] void todo() { throw std::logic_error("not implemented"); }
}  // namespace

Matrix::Matrix(std::size_t /*rows*/, std::size_t /*cols*/, double /*fill*/) { todo(); }

Matrix::Matrix(std::initializer_list<std::initializer_list<double>> /*rows*/) { todo(); }

Matrix Matrix::identity(std::size_t /*n*/) { todo(); }

double& Matrix::operator()(std::size_t /*i*/, std::size_t /*j*/) { todo(); }

double Matrix::operator()(std::size_t /*i*/, std::size_t /*j*/) const { todo(); }

Matrix Matrix::transpose() const { todo(); }

Matrix operator+(const Matrix& /*a*/, const Matrix& /*b*/) { todo(); }
Matrix operator-(const Matrix& /*a*/, const Matrix& /*b*/) { todo(); }
Matrix operator*(const Matrix& /*a*/, const Matrix& /*b*/) { todo(); }
Matrix operator*(double /*s*/, const Matrix& /*a*/) { todo(); }
Vector operator*(const Matrix& /*a*/, const Vector& /*x*/) { todo(); }

bool approx_equal(const Matrix& /*a*/, const Matrix& /*b*/, double /*tol*/) { todo(); }

LU lu_decompose(const Matrix& /*a*/) { todo(); }
Vector solve(const LU& /*f*/, const Vector& /*b*/) { todo(); }
Vector solve(const Matrix& /*a*/, const Vector& /*b*/) { todo(); }
double determinant(const Matrix& /*a*/) { todo(); }
Matrix inverse(const Matrix& /*a*/) { todo(); }
Matrix cholesky(const Matrix& /*a*/) { todo(); }
Vector least_squares(const Matrix& /*a*/, const Vector& /*b*/) { todo(); }

}  // namespace la

#pragma once

#include <Eigen/Core>
#include <iterator>
#include <memory>

namespace VineCopulaUtil {
  template <class Matrix, class T>
  inline void matrix_to_array1d(const Matrix& matrix, T* array1d)
  {
    const int cols = matrix.size();
    const int rows = matrix[0].size();
    
    for (int i = 0 ; i < cols; ++i) {
      std::copy(matrix[i].begin(), matrix[i].end(), array1d);
      array1d += rows;
    }
  }
}// namespace VineCopulaCalculator


template <class ValueType=float, class Matrix>
Eigen::Matrix<ValueType, Eigen::Dynamic, Eigen::Dynamic> STLMatrix2EigenMatrix(const Matrix& matrix)
{
  const int cols = matrix.size();
  const int rows = matrix[0].size();

  std::unique_ptr<ValueType[]> array1d(new ValueType [rows*cols]);
  VineCopulaUtil::matrix_to_array1d(matrix, array1d.get());

  return Eigen::Map<Eigen::Matrix<ValueType, Eigen::Dynamic, Eigen::Dynamic> >(array1d.get(), rows, cols);
}

template <class Vector>
Eigen::Matrix<typename Vector::value_type, Eigen::Dynamic, 1> STLVector2EigenMatrix(Vector& vector)
{
  typedef typename Vector::value_type value_type;
  return Eigen::Map<Eigen::Matrix<value_type, Eigen::Dynamic, 1> >(&vector[0], vector.size(), 1);
}

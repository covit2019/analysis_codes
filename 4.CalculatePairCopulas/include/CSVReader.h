#pragma once

#include <string>
#include <vector>
#include <Eigen/Core>

class CSVReader {
public:
  CSVReader();
  virtual ~CSVReader();

  void Load(const std::string& filename, bool hasHeader=false);
  void PrintCSVInfo();
  int Rows() const {return m_Rows;}
  int Cols() const {return m_Cols;}
  Eigen::MatrixXd GetMatrixXd();
  Eigen::MatrixXd GetMatrixXd(int first_col, int second_col);
private:
  std::vector<std::string> splitString(const std::string &str, char delim);
  long getFileSize();
  std::string strFileSize();
  std::string m_FileName;
  long m_FileSize;
  std::vector<std::vector<std::string>> m_data;
  int m_Cols;
  int m_Rows;
};

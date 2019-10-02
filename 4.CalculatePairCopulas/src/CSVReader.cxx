#include "CSVReader.h"
#include "EigenUtils.hpp"

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <cstdlib>

#define MSG std::cout<<"CSVReader::"<<"\t"
const double KibiByte = 1024.;
const double MebiByte = KibiByte * 1024.;
const double GibiByte = MebiByte * 1024.;
const double TebiByte = GibiByte * 1024.;

//==============================
// CONSTRUCTORS and DESTRUCTORS
//==============================
CSVReader::CSVReader()
{
}
CSVReader::~CSVReader() {}


//==================
// Public Functions
//==================
void CSVReader::Load(const std::string& filename, bool hasHeader)
{
  m_FileName = filename;
  m_FileSize = getFileSize();
  MSG<<"start loading "<<m_FileName<<""<<std::endl;
  m_data.clear();
  
  std::ifstream ifs( m_FileName.c_str() );

  int iRow=0;
  std::string buf;
  while (std::getline(ifs, buf)) {
    ++iRow;
    if (iRow == 1 && hasHeader) continue;

    m_data.push_back( splitString(buf, ',') );
  }
  ifs.close();
  
  m_Rows = m_data.size();
  m_Cols = m_Rows ? m_data[0].size() : 0;
  MSG<<"loading completed."<<std::endl;
}

void CSVReader::PrintCSVInfo()
{
  std::cout<<"======================================="<<"\n";
  std::cout<<"  filename : "<<m_FileName<<"\n";
  std::cout<<"  size     : "<<strFileSize()<<"\n";
  std::cout<<"  columns (=parameters)  : "<<m_Cols<<"\n";
  std::cout<<"  rows    (=samples)     : "<<m_Rows<<"\n";
  std::cout<<"======================================="<<std::endl;
}

Eigen::MatrixXd CSVReader::GetMatrixXd()
{
  std::vector<double> vec;
  for(const auto& row : m_data ) {
    for (const auto& column :row ) {
      vec.push_back( std::stof(column) );
    }
  }
  
  Eigen::MatrixXd d = STLVector2EigenMatrix(vec);
  d.transposeInPlace();
  d.conservativeResize(m_Rows, m_Cols);
  Eigen::MatrixXd d2 = Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>> (d.data(), m_Cols, m_Rows);
  d2.transposeInPlace();
  return d2;
}
  
Eigen::MatrixXd CSVReader::GetMatrixXd(int first_col, int second_col)
{
  std::vector<double> vec;

  for(const auto& row : m_data ) {
    int iCol=-1;
    for (const auto& column : row ) {
      ++iCol;
      if (iCol!=first_col && iCol!=second_col) continue;      
      vec.push_back( std::stof(column) );
    }
  }

  Eigen::MatrixXd d = STLVector2EigenMatrix(vec);
  d.transposeInPlace();
  d.conservativeResize(m_Rows, 2);
  Eigen::MatrixXd d2 = Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>> (d.data(), 2, m_Rows);
  d2.transposeInPlace();
  return d2;
}

//-------------------
// Private Functions
//-------------------
std::vector<std::string> CSVReader::splitString(const std::string &str, char delim)
{
  std::vector<std::string> res;
  size_t current = 0, found;
  while ((found = str.find_first_of(delim, current)) != std::string::npos) {
    res.push_back(std::string(str, current, found - current));
    current = found + 1;
  }
  res.push_back(std::string(str, current, str.size() - current));
  return res;
}

long CSVReader::getFileSize()
{
  std::FILE *fp;
  if ( !(fp = std::fopen(m_FileName.c_str(), "rb")) ) {
    MSG<<"Failed to open "<<m_FileName<<", errno="<<errno<<std::endl;
    return EXIT_FAILURE;
  }
  std::fseek(fp, 0L, SEEK_END);
  long result = std::ftell(fp);
  std::fclose(fp);
  return result;
}

std::string CSVReader::strFileSize()
{
  std::string res;
  std::stringstream ss;
  ss<<std::fixed<<std::setprecision(1);
  if ( m_FileSize > TebiByte ) {
    ss<< m_FileSize / TebiByte << " TiB";
    res = ss.str();
  } else if ( m_FileSize > GibiByte ) {
    ss<< m_FileSize / GibiByte << " GiB";
    res = ss.str();
  } else if ( m_FileSize > MebiByte ) {
    ss<< m_FileSize / MebiByte << " MiB";
    res = ss.str();
  } else if ( m_FileSize > KibiByte ) {
    ss<< m_FileSize / KibiByte << " KiB";
    res = ss.str();
  } else {
    ss<<std::defaultfloat
      << m_FileSize << " Byte";
  }
  ss<<std::defaultfloat;

  return res;
}

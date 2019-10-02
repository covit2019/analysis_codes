#include <vinecopulib.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <chrono>
#include "CSVReader.h"

void usage()
{
  std::cout<<"usage:"<<"\t"<<"PairCopulaCalculator.exe <input csv> <output csv>"<<std::endl;
}

int main(int argc, char* argv[])
{
  if (argc !=3 ) {
    usage();
    return -1;
  }

  const std::string input = argv[1];
  const std::string output = argv[2];
  
  
  CSVReader reader;
  reader.Load(input.c_str());
  reader.PrintCSVInfo();
  
  // Currentry, the calculation of pair copula is executed with default condition
  //===========================================================================================
  // std::vector<vinecopulib::BicopFamily> family_set{vinecopulib::BicopFamily::tll,
  //                                                  vinecopulib::BicopFamily::gaussian};
  // vinecopulib::FitControlsVinecop config(family_set);
  // const std::string selection_criterion("aic");
  // config.set_selection_criterion(selection_criterion);
  // std::cout<<"=======================================\n";
  // std::cout<<" Fitting Configuration \n";
  // std::cout<<"======================================="<<std::endl;
  // std::cout<<"  family_set: ";
  // for (const auto& family : family_set ) {
  //   std::cout<<vinecopulib::get_family_name(family)<<", ";
  // } std::cout<<std::endl;
  // std::cout<<"   criterion: "<<selection_criterion<<std::endl;


  const int n_nodes = reader.Cols();
  
  std::cout<<"start calculating copula..."<<std::endl;
  auto start = std::chrono::system_clock::now(); 

  std::ofstream ofs(output.c_str());
  for (int i=0; i<n_nodes; ++i) {
    for (int j=0; j<n_nodes; ++j) {
      double value = 1.0;
      if (i != j ) {
        Eigen::MatrixXd data = reader.GetMatrixXd(i, j);

        auto bicop = vinecopulib::Bicop(data);
	      // auto bicop = vinecopulib::Bicop(data, config);

	      value = bicop.parameters_to_tau(bicop.get_parameters());
      }
      ofs <<( value<0 ? "": " ") << std::fixed << std::setprecision(8) << value;
      if(j != n_nodes-1) { ofs<<", ";}
    }
    ofs<<std::endl;
  }
  
  auto end = std::chrono::system_clock::now();
  std::cout<<"finished calculating copula..."<<std::endl;
  auto sec = std::chrono::duration_cast<std::chrono::seconds>(end - start).count();
  std::cout <<"  time :"<< sec << " seconds"<<std::endl;  

  return 0;
}

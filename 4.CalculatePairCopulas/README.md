# About 
This package is a driver code for the
+ vinecopulib : https://github.com/vinecopulib/vinecopulib  

The porgram calculates pair-copulas for all columns in the csv file given as a command line arguments.  
And create matrix of Kendall's tau as an output.  


# dependency
## <u>vinecopulib and wdm</u>
vinevopulib is header-only library and enough compact package (Thank you!).
So, to make it easir for use to compile the package, this package includes the part of vinecopulib.
vinecopulib is licensed under the terms of the MIT license. So if you want to copy, see the LICENSE file in the root directory of https://vinecopulib.github.io/vinecopulib/.

And vinecopulib dependes on 
+ wdm https://github.com/tnagler/wdm  (provided by the same author as the vinecopulib)
So, this package also includes the part of wdm as same as the vinecopulib
wdm is also licensed under the terms of the MIT license.
So if you want to copy, please also see the LICENSE file in the root directory of https://vinecopulib.github.io/tragler/wdm


The versions of above packages included in this package are
head version of master branches of 
+ https://github.com/vinecopulib/vinecopulib.git
+ https://github.com/tnagler/wdm.git

at the time of 2019/07/24. The concrete versions are
+ vinecopulib : Release 0.3.2
+ wdm : Release 0.2.0  


## <u>Other packages</u>
You need
+ Boost > 1.56
+ Eigne > 3.3

## Compiler dependency
This package is tested only with g++.


# How to compile
## 1. install required packages
+ ubuntu 18.04 
```
sudo apt install build-essential
sudo apt install libboost-all-dev
sudo apt install libeigen3-dev
```
+ mac os
  + Author is not a user of mac OS, Sorry for if there are some problems
  + Assume that xcode is already installed (it means, you can use g++ command)
```
brew install boost
brew install eigen
```

## 2. compile this packages it self
```
 cd 4.CalculatePairCopulas/cmd
 make
```
then executable binary is created under ./exe directory

# Execute the command
If you are in in cmd direcotry just type
```
 ../exe/PairCopulaCalculator.exe <input_file_name> <output_file_name>
```

# Table of Contents
<!-- TOC -->

- [Table of Contents](#table-of-contents)
- [About this package](#about-this-package)
- [Overview of experiment procedures](#overview-of-experiment-procedures)
  - [Environment](#environment)
- [How to run the programs](#how-to-run-the-programs)
  - [<u>1. Train a neural network</u>](#u1-train-a-neural-networku)
  - [<u>2. Create PDF and CDF distributions for each node in the trained neural network.</u>](#u2-create-pdf-and-cdf-distributions-for-each-node-in-the-trained-neural-networku)
    - [Create PDF/CDF distributions (Fill the histograms)](#create-pdfcdf-distributions-fill-the-histograms)
    - [Create figures](#create-figures)
  - [<u>3. Prepare the input files to calculate copulas</u>](#u3-prepare-the-input-files-to-calculate-copulasu)
  - [<u>4. Estimate copulas and dump coefficient correlation matrix</u>](#u4-estimate-copulas-and-dump-coefficient-correlation-matrixu)
  - [<u>5. Analyze the correlation matrix</u>](#u5-analyze-the-correlation-matrixu)

<!-- /TOC -->

# About this package
This package contains source codes for the experiment using Copula-based Visualization Techniques.
The source codes and its results are included except for the executable to compute copulas.
The program to compute copulas is written in C++, so you need to compile it with your environments. 
More details to compile the programs are explained in *4.CalculatePairCopulas/README.md*.

# Overview of experiment procedures
You need 5 steps to get the results.
1. Train a neural network.
2. Make CDF distributions for all nodes in the trained neural network.
3. Prepare the input files to calculate copulas.
4. Estimate copulas among the nodes and create a coefficient correlation matrix.
5. Analyze the obtained coefficient correlation matrix 

Basically, Only you need to do is run the scripts/executable sequentially from

+ 1.ModelingNN  

Before running the script written in python, you have to install some dependent packages(numpy, pandas, matplot, tensorflow,...) via pip command.
Note that the version tensorflow used in this analysis is 2.0.0-beta, not a version 1.X.
You also need ROOT ( https://root.cern.ch/ ) which is a scientific software toolkit developed at CERN.
Although you can not install ROOT via pip command, but you can install it easily via conda command if you are using anaconda as python environment.
See https://github.com/conda-forge/root-feedstock/ for more details about installing root.

+ 00.DotFilesToCreateFigures

contains scripts for GraphViz to make some figures such as graph structure of a neural network. And not necessary for the experiment.

## Environment
The author using these analysis codes with the following environment
+ python 3.7 created with anaconda as python environment
+ g++ 7.4 as C++ compiler


# How to run the programs
## <u>1. Train a neural network</u>  
Just type the following commands in your terminal

    > cd 1.ModelingNN
    > python train_nn_for_Iris.py
Then the bellow files will be created.

+ iris_nn_model.png : Summary of the neural network model
+ train.log : log of training for each epoch
+ learning_curve.png : learning curve
+ iris_nn_outputs.csv : input features and the output of activation functions for each node of hidden layers and prediction results in the neural netwrok for each sample.


## <u>2. Create PDF and CDF distributions for each node in the trained neural network.</u>  
### 2.1 Create PDF/CDF distributions (Fill the histograms)
Due to the number of samples is not large, we handle PDF and CDF distributions as histograms in this analysis.
To make the PDF and CDF distributions, type the following commands in your terminal

    > cd 2.CreatePDFandCDF
    > python make_iris_distibutions.py
Then the bellow files will be created.
Note that your need *iris_nn_ouputs.csv* which is created in the previous step in the working directory.
+ dist_all.root
+ dist_y_0.root
+ dist_y_1.root
+ dist_y_2.root

The created histograms are stored in the above files.

### 2.2 Create figures
To create figures from histograms in the root files. Just type

    > python distributions2figures.py

What this script is just visualizing the histograms. So this process is not necessary, just exists for validation.
Note that the script assumes that the directory with name *fig* exists in the working directory. 

## <u>3. Prepare the input files to calculate copulas</u>  
What is doing in this process is just to calculate the CDF value for all nodes in the neural network for each sample. 
To run the script, first, copy the following files created in the previous steps into the *3.CreateInputForvineCopulib* directory
+ iris_nn_ouputs.csv
+ dist_all.root
+ dist_y_0.root
+ dist_y_1.root
+ dist_y_2.root

And type the following command

    > cd 3.CreateInputForvineCopulib
    > python ./make_input_for_vinecopulib.py

Then
+ for_vinecopulib_all.csv

will be created. This csv file includes the value of CDF value for each node of the neural network and will be the input file for copula estimation.

## <u>4. Estimate copulas and dump coefficient correlation matrix</u> 
In this procedure, the program estimates pair-copulas for each node in the neural network. Then, we consider Kendall's tau for each pair-copulas as the coefficient correlation.
To estimate the copula, this package using noble library [vinecopulib](https://github.com/vinecopulib/vinecopulib). 

Before running the program, you need to compile the executable.
You need Boost and Eigen before compiling the program.
If you need more details, please read  
*4.CalculatePairCopulas/README.md*

To compile and run the package, please do as follows

    > cd 4.CalculatePairCopulas/cmd
    > make
    > cd ../run
    > ../exe/PairCopulaCalculator.exe ./for_vinecopulib_all.csv ./iris_CM.csv


*./for_vinecopulib_all.csv* is an input for copula estimation.
You should specify the file created in step 3.
Then you can obtain the output *iris_CM.csv*.
This file contains a table of Kendall's tau for each pair-copulas and we treat this table as a coefficient correlation matrix between the  
of the nodes in the trained neural network. In the next step, we analyze this correlation matrix.

## <u>5. Analyze the correlation matrix</u>
The following two files are sub moduled called from the main analysis script.
+ NodeStructure.py
+ NNCorrelationMatrix.py

To run the main analysis script, do as follows

    > cd 5.AnalyzeCorrelationMatrix
    > python ./Iris_NN_copula_analysis.py ./iris_CM.csv ./nodes_4_6_6_3.txt

The 1st argument *iris_CM.csv* is a table of Kendall's tau created in step 4.
And 2nd argument *nodes_4_6_6_3.txt is a text file that indicates the structure of the neural network.

The following results will be printed out to the standard output.
+ table of Kendall's tau
+ sensitive paths
+ importance of input features
+ part of .dot script to visualize the importance of paths

And the following files are created as the output.
+ CM.png : a heatmap of Kendall's tau 
+ paths_sorted_by_variance.csv : CCC and VaR(CCC) for all paths sorted by order of VaR(CCC)

To obtain the feature importance by Random Forst for comparison.
Please run the script as follows 

    > python ./rf_for_Iris.py

Then the importance of features will be printed on the standard output.
To make the comparison plots, you can run the script as follows

    > python ./compare_importance.py

Then the output file

+ comparison_with_RF.pdf

will be created.
Note that the results of each algorithm are hardcoded in *compare_importance.py*.
If you change the experimental condition, you need to copy the results.

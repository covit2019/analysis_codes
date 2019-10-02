# AISTAT2020

# Contents 
The source codes and the results are included except executable to compute copulas.
The programm to compute copulas is wittern in C++、and you should compile it with your own environments,
The executable itself is not included.


# Experiment procedures
Basycally, just run the python codes sequentially from

+ 1.ModelingNN  

Before run the python codes, you have to install some dependent packages(numpy, pandas, matplot, tensorflow,...) via pip command.
Note that the version tensorflow used in this analysis tensorflow 2.0.0-beta.
Also, you also need ROOT ( https://root.cern.ch/ ) which is a modular scientific software toolkit developed at CERN.
Alothough you can not install ROOT via pip command, but you can install it easily via conda command if you are using anaconda as python environment.
See https://github.com/conda-forge/root-feedstock/ for more details about installing root.

+ 00.DotFilesToCreateFigures

includes .dot scripts to make figures such as graph structure of neural network.
## environments 
Author use
+ anaconda as python environment
+ g++ as C++ compiler

# How to run

## <u>1.ModelingNN</u>  
Just type the following commands in your terminal

    > cd 1.ModelingNN
    > python train_nn_for_Iris.py
Then the bellow files will be created.

+ iris_nn_model.png : Summary of neural network model
+ train.log : log of training for each epcoh
+ learning_curve.png : learning curve
+ iris_nn_outputs.csv : input features and the output of activation functions for each node of hidden leayers and prediction results in the neural netwrok for each samples.


## <u>2.CreatePDFandCDF</u>  
### 2.1 fill the histogram (create PDF/CDF ditributions)
Just type the following commands in your terminal

    > cd 2.CreatePDFandCDF
    > python make_iris_distibutions.py
Then the bellow files will be created.
Note that your need *iris_nn_ouputs.csv* which is created in the previous step in the working directory.
+ dist_all.root
+ dist_y_0.root
+ dist_y_1.root
+ dist_y_2.root

The histograms are included in the above files.

### 2.2 create figures
To create figures from histograms in the root files. Just type as 

    > python distributions2figures.py

と打つだけです。
Note that the script assume that the directory with name *fig* exist in the working directory. 

## <u>3.CreateInputForvineCopulib</u>  
Copy the following files created in the previous steps into the *3.CreateInputForvineCopulib*
+ iris_nn_ouputs.csv
+ dist_all.root
+ dist_y_0.root
+ dist_y_1.root
+ dist_y_2.root

Then, type the following command

    > cd 3.CreateInputForvineCopulib
    > python ./make_input_for_vinecopulib.py

+ for_vinecopulib_all.csv

will be created. This csv file includes the value of cdf for each node of the neural network and will be the input file for copula estimation.

## <u>4.CalculatePairCopulas</u> 
You need to install boost and eigen before compile the package.
For this step, see  
4.CalculatePairCopulas/README.md 
for more details.

To compile and run the package, please do as follows

    > cd 4.CalculatePairCopulas/cmd
    > make
    > cd ../run
    > ../exe/PairCopulaCalculator.exe ./for_vinecopulib_all.csv ./iris_CM.csv


*./for_vinecopulib_all.csv* is input for copula estimation.
So you should specify the file create in the step 3.
Then you can obtaine the output *iris_CM.csv* .
This is a table of Kendall's tau and we treat this tables as correlation matrix 
of the node in the neural network. In the next step, we analyze this correlation matrix.

## <u>5.AnalyzeCorrelationMatrix</u>
The following two files are called from main analysis script.
+ NodeStructure.py
+ NNCorrelationMatrix.py

To run the main analysis script, do as follows

    > cd 5.AnalyzeCorrelationMatrix
    > python ./Iris_NN_copula_analysis.py ./iris_CM.csv ./nodes_4_6_6_3.txt

The 1st argument *iris_CM.csv* is table of Kendall's tau cretated in the step4.
And 2nd argument *nodes_4_6_6_3.txt is a text file which indicate the structure of the neural network.

The following results are printed out to the standard output.
+ table of Kendall's tau
+ sensitive paths
+ importance of input features
+ part of .dot script to visualize the importance of paths

And following files are created as the result.
が画面に表示されます。また同時に以下のファイルが作成されます
+ CM.png : heatmap of Kendall's tau 
+ paths_sorted_by_variance.csv : CCC and VaR(CCC) for all paths sorted by order of VaR(CCC)

To obtain the feature importance by Random Forst for comparison.
Please run the script as follows 

    > python ./rf_for_Iris.py

Then the importnace of features will be printed on the standard output.
To make the comparison plots, you can run the script as follows

    > python ./compare_importance.py

Then the ouput file

+ comparison_with_RF.pdf

will be created.
Note that, the results of each algorithm are hard coded in the above scripts.
If you change the experimatal condition, you need to copy the results.

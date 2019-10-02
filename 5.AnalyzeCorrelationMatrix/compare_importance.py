from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np

# Results of each methods obtained from stdout of
# - Iris_NN_copula_analysis.py
# - rf_for_Iris.py
#-----------------------------------------------------------------------
#                       x_0,        x_1,        x_2,        x_3
#-----------------------------------------------------------------------
result_copula_method = [0.15991334, 0.00211143, 0.41839555, 0.41957968]
result_random_forest = [0.13641555, 0.03178982, 0.4118627,  0.41993193]


def visualization(result_copula_method, result_random_forest, labels):
  plt.figure(figsize = (12,4))
  offset = np.arange(len(result_copula_method))
  bar_width = 0.3
  plt.barh(offset, result_copula_method, color='r', height=bar_width, align='center', label='CoViT')
  plt.barh(offset + bar_width, result_random_forest, color='b', height=bar_width, align='center', label='Random Forest')
  plt.yticks(offset + bar_width/2, labels)
  plt.legend(fontsize=15)
  plt.tick_params(labelsize=15)
  plt.savefig('comparison_with_RF.pdf')

def sort_results(result_copula_method, result_random_forest, labels):
  result = [[],[],[]]
  for i in np.argsort( np.array(result_copula_method) ):
    result[0].append( result_copula_method[i] )
    result[1].append( result_random_forest[i] )
    result[2].append( labels[i] )
  return result


if __name__ == '__main__':
  iris = datasets.load_iris()
  #labels = iris.feature_names
  labels = ["sepal\nlength", "sepal\nwidth", "petal\nlength", "petal\nwidth"]
  result = sort_results(result_copula_method, result_random_forest, labels)
  visualization( result[0], result[1], result[2] )

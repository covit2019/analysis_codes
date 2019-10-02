import NodeStructure as ns

import pandas as pd
import numpy as np
#from operator import itemgetter
from copy import deepcopy
import matplotlib.pyplot as plt
import seaborn as sns

class NNCorrelationMatrix():
  def __init__(self, name, cm_file, node_file):
    self.__name = name
    self.__full_CM = pd.read_csv(cm_file, header=None)
    self.__network = ns.NodeStructure(node_file)

    if self.__full_CM.shape[0] != self.__network.n_params():
      print('!! number of parameters are inconsistent between two csv files !!')

    tmp_columns = []
    for layer in self.__network.layers():
      for node in layer:
        
        tmp_columns.append(node)
    self.__full_CM.columns = tmp_columns
    self.__full_CM.index = tmp_columns


  def show_cm(self):
    print(self.__full_CM)


  def draw_cm(self):
    plt.figure(figsize = (10,7))

    ax = sns.heatmap(self.__full_CM, square=True, annot=True, vmin=-1, vmax=1, cmap='jet')#, xticklabels=label, yticklabels=label)
    new_yticks = [t - 0.5 for t in ax.get_yticks()]
    new_yticks.append(ax.get_yticks()[-1] + 0.5)
    ax.set_yticks(new_yticks, minor=True)
    plt.title("Correlation Matrix")

    plt.savefig("./" + self.__name + ".png")  


  def show_layers(self):
    self.__network.show()


  def products_to_node(self, node):
    res = []
    routes = self.__network.route_to_node(node)
    #print('routes ->\n', routes)
    for route in routes:
      product = 1.
      for i in range(1, len(route)):
        product *= self.__full_CM[route[i-1]][route[i]]
      #res.append( (route, product) )
      res.append( (route[1:], product) )
    return res


if __name__ == '__main__':
  CM = NNCorrelationMatrix('CM', './iris_all_CM.csv', './nodes.txt')
  CM.show_cm()
  print("")
  CM.draw_cm()

  #CM.show_layers()
  products_pred0 = pd.DataFrame(CM.products_to_node("pred_0"))
  products_pred1 = pd.DataFrame(CM.products_to_node("pred_1"))
  products_pred2 = pd.DataFrame(CM.products_to_node("pred_2"))

  products_pred0.columns = ["reversed_path", "pred_0"]
  products_pred1.columns = ["reversed_path", "pred_1"]
  products_pred2.columns = ["reversed_path", "pred_2"]

  n_labels = 3
  products = deepcopy(products_pred0)
  products["pred_1"] = deepcopy(products_pred1["pred_1"])
  products["pred_2"] = deepcopy(products_pred2["pred_2"])
  products["mean"] = (products["pred_0"] + products["pred_1"] + products["pred_2"]) / n_labels
  products["deviation"] = np.sqrt( ((products["pred_0"]-products["mean"])**2 + (products["pred_1"]-products["mean"])**2 + (products["pred_2"]-products["mean"])**2) / (n_labels-1))
  products["sigma_0"] = (products["pred_0"] - products["mean"]) / products["deviation"]
  products["sigma_1"] = (products["pred_1"] - products["mean"]) / products["deviation"]
  products["sigma_2"] = (products["pred_2"] - products["mean"]) / products["deviation"]
  products["abs_sigma_0"] = np.abs( products["sigma_0"] )
  products["abs_sigma_1"] = np.abs( products["sigma_1"] )
  products["abs_sigma_2"] = np.abs( products["sigma_2"] )

  products = products.sort_values("deviation", ascending=False)
  products.to_csv("products_of_correlation_sorted_by_deviation.csv", index=None)
  print( products.head(10) )

  products = products.sort_values("abs_sigma_0", ascending=False)
  products.to_csv("products_of_correlation_sorted_by_sigma_0.csv", index=None)
  products = products.sort_values("abs_sigma_1", ascending=False)
  products.to_csv("products_of_correlation_sorted_by_sigma_1.csv", index=None)
  products = products.sort_values("abs_sigma_2", ascending=False)
  products.to_csv("products_of_correlation_sorted_by_sigma_2.csv", index=None)

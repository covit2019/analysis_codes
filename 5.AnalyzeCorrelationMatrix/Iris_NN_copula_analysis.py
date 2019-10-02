from NNCorrelationMatrix import NNCorrelationMatrix
import sys
import pandas as pd
import numpy as np
from copy import deepcopy
import cv2

def calc_deviations(CCC_pred0, CCC_pred1, CCC_pred2):
  n_labels = 3
  CCC = deepcopy(CCC_pred0)
  CCC["pred_1"] = deepcopy(CCC_pred1["pred_1"])
  CCC["pred_2"] = deepcopy(CCC_pred2["pred_2"])
  CCC["input"] = CCC['reversed_path'].apply(lambda x: x[-1])
  CCC["mean"] = (CCC["pred_0"] + CCC["pred_1"] + CCC["pred_2"]) / n_labels
  CCC["deviation"] = np.sqrt( ((CCC["pred_0"]-CCC["mean"])**2 + (CCC["pred_1"]-CCC["mean"])**2 + (CCC["pred_2"]-CCC["mean"])**2) / (n_labels-1))
  CCC["VaR(CCC)"] = ((CCC["pred_0"]-CCC["mean"])**2 + (CCC["pred_1"]-CCC["mean"])**2 + (CCC["pred_2"]-CCC["mean"])**2) / (n_labels-1)
  return CCC


def make_output(CCC):
  CCC = CCC.sort_values("VaR(CCC)", ascending=False)
  CCC.to_csv("paths_sorted_by_variance.csv", index=None)
  print("========== Top 10 List of Convolution of Correlation (ranking by VaR(CCC)) ==========")
  print( CCC.head(10) )
  print("\n")
  print_pseudo_importancs(CCC)


def print_pseudo_importancs(CCC):
  res = []
  res.append( np.square(CCC[CCC["input"]=="x_0"]["VaR(CCC)"]).mean() )
  res.append( np.square(CCC[CCC["input"]=="x_1"]["VaR(CCC)"]).mean() )
  res.append( np.square(CCC[CCC["input"]=="x_2"]["VaR(CCC)"]).mean() )
  res.append( np.square(CCC[CCC["input"]=="x_3"]["VaR(CCC)"]).mean() )

  res = np.array(res)
  res = res / np.sum(res)
  print("========== Imnportance estimated by CoVit ==========")
  print(res)


def integrate_paths(CCC):
  result = {}

  for iPath in range( CCC.values.shape[0] ):
    deviation = CCC["VaR(CCC)"][iPath]
    path = CCC.values[iPath][0] 
    edge = (path[2], path[1])
    result[edge] = result[edge] + deviation if edge in result else deviation
    edge = (path[1], path[0])
    result[edge] = result[edge] + deviation if edge in result else deviation

  max_v = max( result.values() )
  min_v = min( result.values() )


  print("========== Visualize importance of edges ==========")
  print(" Just copy the below results to your .dot file ")
  for k, v in result.items():
    h = 1 - (v-min_v) / (max_v -min_v) 
    r, g, b = hsv_to_rgb(h* 120.)
    val = '#%02X%02X%02X' % (r,g,b)
    if h > 0.7:
      val += '19'

    print('{' + k[0] + '} -> {' + k[1] + '} [color="' + val + '"]')#, h, r, g, b)

    img = np.zeros((30, 300, 3), dtype=np.uint8)
    for i in range(100):
      col = np.array( hsv_to_rgb( i*0.01 * 120.) )
      for j in range(30):
        img[j][i*3] = col
        img[j][i*3+1] = col
        img[j][i*3+2] = col
    cv2.imwrite("colorbar.png", img)


def hsv_to_rgb(h, s=255, v=255):
    bgr = cv2.cvtColor(np.array([[[h, s, v]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
    return (bgr[2], bgr[1], bgr[0])



def main(argvs):
  CM = NNCorrelationMatrix('CM', argvs[1], argvs[2])
  print("========== Correlation Matrix ==========")
  CM.show_cm()
  print("\n")
  CM.draw_cm()

  CCC_pred0 = pd.DataFrame(CM.products_to_node("pred_0"))
  CCC_pred1 = pd.DataFrame(CM.products_to_node("pred_1"))
  CCC_pred2 = pd.DataFrame(CM.products_to_node("pred_2"))
  CCC_pred0.columns = ["reversed_path", "pred_0"]
  CCC_pred1.columns = ["reversed_path", "pred_1"]
  CCC_pred2.columns = ["reversed_path", "pred_2"]
  CCC = calc_deviations(CCC_pred0, CCC_pred1, CCC_pred2)
  make_output(CCC)
  print("\n")

  integrate_paths(CCC)

if __name__ == "__main__":
  argvs = sys.argv
  if len(argvs) != 3:
    print("Useage:\n")
    print("$python ./Iris_NN_copula_analysis.py <Correlation Matrix file> <Node Structur file>")
    exit(1)

  main(argvs)

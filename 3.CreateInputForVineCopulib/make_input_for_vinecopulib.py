from ROOT import TFile, TH1D, TCanvas, gStyle, THStack, kRed, kGreen, kBlue, kBlack, TLegend, gPad
import pandas as pd
import numpy as np

def load_distributions():
  f_all = TFile('dist_all.root')
  f_0   = TFile('dist_y_0.root')
  f_1   = TFile('dist_y_1.root')
  f_2   = TFile('dist_y_2.root')
  return f_all, f_0, f_1, f_2

def load_data(cvsfile, label=-1):
  df = pd.read_csv(cvsfile)
  if label < 0:
    return df
  else:
    df = df[(df.true_y==label) & (df.pred_y==label)]
  return df

def get_hist(file, histname):
  return file.Get(histname)

def raw_output_to_cdf(file, key, data):
  cdf = []
  h = get_hist(file, key+'_cdf')
  nBins = h.GetNbinsX()
  for x in data:
    iBin = h.FindBin(x)
    if iBin == 0:
      cdf.append(0.)
    elif iBin > nBins:
      cdf.append(1.)
    else:
      cdf.append(h.GetBinContent(iBin))

  return np.array(cdf)


if __name__ == "__main__":
  gStyle.SetOptStat(0)
  # Load pdf/cdf distribution for trained NN
  #   f_all : pdf/cdf is obtained from all samle
  #   f_i : for sample which both of truth and predicted y == i
  #=============================================================
  f_all, f_0, f_1, f_2 = load_distributions()

  # Load raw output of each node of the NN
  # in prediction time
  #============================================
  df_all = load_data('iris_nn_outputs.csv')
  #df_y_0 = load_data('iris_nn_outputs.csv', 0)
  #df_y_1 = load_data('iris_nn_outputs.csv', 1)
  #df_y_2 = load_data('iris_nn_outputs.csv', 2)


  out_all = pd.DataFrame()
  #out_y_0 = pd.DataFrame()
  #out_y_1 = pd.DataFrame()
  #out_y_2 = pd.DataFrame()
  for key in df_all.columns[:-2]:
    out_all[key] = raw_output_to_cdf(f_all, key, df_all[key].values)
    #out_y_0[key] = raw_output_to_cdf(f_all, key, df_y_0[key].values)
    #out_y_1[key] = raw_output_to_cdf(f_all, key, df_y_1[key].values)
    #out_y_2[key] = raw_output_to_cdf(f_all, key, df_y_2[key].values)

  out_all.to_csv('for_vinecopulib_all.csv', index=None, header=None)
  #out_y_0.to_csv('for_vinecopulib_y_0.csv', index=None, header=None)
  #out_y_1.to_csv('for_vinecopulib_y_1.csv', index=None, header=None)
  #out_y_2.to_csv('for_vinecopulib_y_2.csv', index=None, header=None)
 
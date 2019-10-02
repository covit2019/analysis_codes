import pandas as pd
from ROOT import TFile, TH1D, TCanvas

def load_data(cvsfile, label=-1):
  df = pd.read_csv(cvsfile)
  if label < 0:
    return df
  else:
    df = df[(df.true_y==label) & (df.pred_y==label)]
  return df


def make_hist_from_DataFrame(df, key, title, nBins, low, high):
  h = TH1D(key, title, nBins, low, high)
  for x in df[key]:
    h.Fill(x)
  return h

def pdf_hist(df, key, nBins, low, high):
  # This function is called from creaet_distribution() via make_plots()
  # In this function, histogram is not normalized and normalization is applyed in creaet_distribution() 
  # So, the return value of this function is not a PDF
  h = make_hist_from_DataFrame(df, key, key+';x;P(x)', nBins, low, high)
  return h

def pdf2cdf(original_pdf):
  pdf = original_pdf.Clone()
  pdf.Scale(1./original_pdf.GetEntries())
  nBins = pdf.GetNbinsX()
  binWidth = pdf.GetBinWidth(nBins)
  xMin = pdf.GetBinCenter(1) - 0.5 * binWidth
  xMax = pdf.GetBinCenter(nBins) + 0.5 * binWidth
  h = TH1D(pdf.GetName()+'_cdf', 'cdf_'+pdf.GetName()+';x;#int P(x)dx', nBins, xMin, xMax)
  for iBin in range(1, nBins+1):
    h.SetBinContent( iBin, pdf.Integral(0, iBin) )
  return h

def make_plots(key, nBins, df, df_all):
  pdf = pdf_hist(df, key, nBins, df_all[key].min(), df_all[key].max())
  # pdf is not normalized yet, so to ensure that range of cdf == [0,1]
  # normalize the pdf for 
  cdf = pdf2cdf(pdf)

  return pdf, cdf

def create_distribution(output, df, df_all):
  f_output = TFile(output, 'recreate')
  for key in df.columns[:-2]:
    # Skip last two columns (true label & predicted label)
    # because these are not an output of node
    #--------------------------------------------
    pdf, cdf = make_plots(key, 20, df, df_all)
    if pdf.GetBinWidth(1)>0:
      pdf.Scale(1./df_all.size / pdf.GetBinWidth(1))
    else:
      pdf.Scale(1./df_all.size)
    pdf.Write()
    cdf.Write()

  f_output.Write()


if __name__ == '__main__':
  df_all = load_data('iris_nn_outputs.csv')
  df_0 = load_data('iris_nn_outputs.csv', 0)
  df_1 = load_data('iris_nn_outputs.csv', 1)
  df_2 = load_data('iris_nn_outputs.csv', 2)
  create_distribution('dist_all.root', df_all, df_all)
  create_distribution('dist_y_0.root', df_0, df_all)
  create_distribution('dist_y_1.root', df_1, df_all)
  create_distribution('dist_y_2.root', df_2, df_all)

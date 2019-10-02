from ROOT import TFile, TH1D, TCanvas, gStyle, THStack, kRed, kGreen, kBlue, kBlack, TLegend, gPad

f_all = TFile('dist_all.root')
f_0   = TFile('dist_y_0.root')
f_1   = TFile('dist_y_1.root')
f_2   = TFile('dist_y_2.root')

def getHist(file, histname):
  h = file.Get(histname)
  #print( h )
  return h

def make_pdf_plot(key, pos=(0.7,0.7,0.9,0.9)):
  h = getHist(f_all, key)
  h.SetLineStyle(1)
  h.SetLineWidth(5)
  #h.SetFillStyle(1001)
  h.SetLineColor(kBlack)

  hs = THStack("hs_"+key, "")
  h0 = getHist(f_0, key)
  h1 = getHist(f_1, key)
  h2 = getHist(f_2, key)

  h0.SetLineStyle(5)
  h0.SetFillStyle(3005)
  h0.SetFillColor(kRed)
  h0.SetLineColor(kRed)
  hs.Add(h0)
  h1.SetLineStyle(5)
  h1.SetFillStyle(3005)
  h1.SetFillColor(kBlue)
  h1.SetLineColor(kBlue)
  hs.Add(h1)
  h2.SetLineStyle(5)
  h2.SetFillStyle(3005)
  h2.SetFillColor(kGreen)
  h2.SetLineColor(kGreen)
  hs.Add(h2)
  leg = TLegend(pos[0],pos[1],pos[2],pos[3])
  leg.AddEntry(h,  'total')
  leg.AddEntry(h0, 'y == Pred == 0')
  leg.AddEntry(h1, 'y == Pred == 1')
  leg.AddEntry(h2, 'y == Pred == 2')
  return h, hs, leg

def make_cdf_plot(key, pos=(0.7,0.1,0.9,0.3)):
  h = getHist(f_all, key)
  h.SetLineStyle(1)
  h.SetLineWidth(5)
  h.SetLineColor(kBlack)

  h0 = getHist(f_0, key)
  h1 = getHist(f_1, key)
  h2 = getHist(f_2, key)

  h0.SetLineStyle(5)
  h0.SetLineColor(kRed)
  h1.SetLineStyle(5)
  h1.SetLineColor(kBlue)
  h2.SetLineStyle(5)
  h2.SetLineColor(kGreen)

  leg = TLegend(pos[0],pos[1],pos[2],pos[3])
  leg.AddEntry(h,  'total')
  leg.AddEntry(h0, 'y == Pred == 0')
  leg.AddEntry(h1, 'y == Pred == 1')
  leg.AddEntry(h2, 'y == Pred == 2')
  return (h, h0, h1, h2), leg


def draw(keys, figname):
  size = (len(keys), 2)
  c = TCanvas("c", "", size[0]*400, size[1]*400)
  c.Divide(size[0], size[1])

  h = [None] * len(keys)
  hs = [None] * len(keys)
  leg = [None] * len(keys)
  cdf = [None] * len(keys)
  for i, key in enumerate(keys):
    c.cd(i + 1)
    h[i], hs[i], leg[i] = make_pdf_plot(key)
    h[i].Draw('hist')
    hs[i].Draw('hist same')
    leg[i].Draw('hist same')

    c.cd(i + size[0] + 1)
    cdf[i], l = make_cdf_plot(key + '_cdf')
    cdf[i][0].SetMinimum(0)
    cdf[i][0].SetMaximum(1.1)
    cdf[i][0].Draw("hist")
    cdf[i][1].Draw("hist same")
    cdf[i][2].Draw("hist same")
    cdf[i][3].Draw("hist same")
    l.Draw()
  c.SaveAs(figname)


def draw_pdf_vertical(keys, figname):
  size = (1, len(keys))
  c = TCanvas("c", "", size[0]*400, size[1]*400)
  c.Divide(size[0], size[1])

  h = [None] * len(keys)
  hs = [None] * len(keys)
  leg = [None] * len(keys)
  cdf = [None] * len(keys)
  for i, key in enumerate(keys):
    c.cd(i + 1)
    h[i], hs[i], leg[i] = make_pdf_plot(key)
    h[i].Draw('hist')
    hs[i].Draw('hist same')
    leg[i].Draw('hist same')

  c.SaveAs(figname)

if __name__ == '__main__':
  gStyle.SetOptStat(0)

  draw(["x_0", "x_1", "x_2", "x_3"], './fig/InputLayer.png')
  draw(["h0_0", "h0_1", "h0_2", "h0_3", "h0_4", "h0_5"], './fig/HiddenLayer0.png')
  draw(["h1_0", "h1_1", "h1_2", "h1_3", "h1_4", "h1_5"], './fig/HiddenLayer1.png')
  draw(["pred_0", "pred_1", "pred_2"], './fig/OutputLayer.png')

  draw_pdf_vertical(["x_0", "x_1", "x_2", "x_3"], './fig/InputLayer_pdf.png')
  draw_pdf_vertical(["h0_0", "h0_1", "h0_2", "h0_3", "h0_4", "h0_5"], './fig/HiddenLayer0_pdf.png')
  draw_pdf_vertical(["h1_0", "h1_1", "h1_2", "h1_3", "h1_4", "h1_5"], './fig/HiddenLayer1_pdf.png')
  draw_pdf_vertical(["pred_0", "pred_1", "pred_2"], './fig/OutputLayer_pdf.png')

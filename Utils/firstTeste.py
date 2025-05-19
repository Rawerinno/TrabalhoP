import ROOT

myFile = ROOT.TFile("/home/cotton/Utils/TrabalhoPraticoUtils/AmberTarget_Run_0.root", "READ")
myFile.ls()
vertexTree=myFile.Get("hadronicVertex")
vertexTree.Print()
histogram=ROOT.TH1D("primaryVertex","primaryVertex",400,-400,0)   
vertexTree.Draw("vertexPosZ_cm>>primaryVertex","IsPrimary==1","goff")
histogram.SetLineColor(ROOT.kRed)
histogram.Draw()
histogram.SaveAs("histogram.png")
# h = ROOT.TH1F("myHist", "myTitle", 64, -4, 4)
# h.FillRandom("gaus")
# h.Draw()

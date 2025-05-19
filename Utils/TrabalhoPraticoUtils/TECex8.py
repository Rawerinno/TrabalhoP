import ROOT

# Abrir ficheiro e árvore
file = ROOT.TFile.Open("AmberTarget_Run_0.root")
tree = file.Get("Hits")

# Criar histogramas
h_muon = ROOT.TH1F("h_muon", "pZ dos muões; pZ [GeV]; Contagem", 3000, 0, 50)
h_pion = ROOT.TH1F("h_pion", "pZ dos piões; pZ [GeV]; Contagem", 3000, 0, 50)

# Preencher histogramas com cortes
tree.Draw("pZ_GeV >> h_muon", "abs(particlePDG) == 13")
tree.Draw("pZ_GeV >> h_pion", "abs(particlePDG) == 211")

# Desenhar ambos
c = ROOT.TCanvas()
h_muon.SetLineColor(ROOT.kBlue)
h_pion.SetLineColor(ROOT.kRed)

h_muon.Draw()
h_pion.Draw("SAME")

legend = ROOT.TLegend()
legend.AddEntry(h_muon, "Muões", "l")
legend.AddEntry(h_pion, "Piões", "l")
legend.Draw()

#c.SaveAs("pZ_muons_vs_pions.png")

input("Pressione Enter para sair...")

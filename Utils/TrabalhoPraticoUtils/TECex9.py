import ROOT

# Abrir ficheiro e árvore
file = ROOT.TFile.Open("AmberTarget_Run_3.root")
tree = file.Get("Hits")

# Criar histogramas
h_prim = ROOT.TH1F("h_prim", "pZ dos piões primários; pZ [GeV]; Contagem", 1000, -1, 500)
h_sec = ROOT.TH1F("h_sec", "pZ dos piões secundários; pZ [GeV]; Contagem", 1000, -1, 500)


# Preencher
tree.Draw("pZ_GeV >> h_prim", "abs(particlePDG) == 211 && IsPrimary == 1")
tree.Draw("pZ_GeV >> h_sec", "abs(particlePDG) == 211 && IsPrimary == 0")

# Desenhar
c = ROOT.TCanvas()
h_prim.SetLineColor(ROOT.kGreen+2)
h_sec.SetLineColor(ROOT.kOrange+7)

h_prim.Draw()
h_sec.Draw("SAME")

legend = ROOT.TLegend()
legend.AddEntry(h_prim, "Piões primários", "l")
legend.AddEntry(h_sec, "Piões secundários", "l")
legend.Draw()

#c.SaveAs("pZ_pions_primary_secondary.png")

input("Pressione Enter para sair...")
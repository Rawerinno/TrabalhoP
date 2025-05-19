import ROOT

# Abrir o ficheiro ROOT
file = ROOT.TFile("AmberTarget_Run_0.root")
tree = file.Get("tracksData")

# Verificar se a árvore foi carregada
if not tree:
    raise RuntimeError("A árvore 'tracksData' não foi encontrada no ficheiro ROOT.")

# Criar histogramas
hist_muon = ROOT.TH1F("hist_muon", "Energia Total - Muões;Energia Total (keV);Contagem", 100, 0, 50000)
hist_pion = ROOT.TH1F("hist_pion", "Energia Total - Piões;Energia Total (keV);Contagem", 100, 0, 50000)
hist_others = ROOT.TH1F("hist_others", "Energia Total - Outras Partículas;Energia Total (keV);Contagem", 100, 0, 1000)

# Fórmula da energia total depositada nos detectores
edep_total_expr = "EdepDet0_keV + EdepDet1_keV + EdepDet2_keV + EdepDet3_keV"

# Preencher histogramas com base no tipo de partícula (particlePDG)
tree.Draw(f"{edep_total_expr} >> hist_muon", "particlePDG == 13", "goff")
tree.Draw(f"{edep_total_expr} >> hist_pion", "particlePDG == 211", "goff")
tree.Draw(f"{edep_total_expr} >> hist_others", "particlePDG != 13 && particlePDG != 211", "goff")

# Estilo
hist_muon.SetLineColor(ROOT.kBlue)
hist_pion.SetLineColor(ROOT.kRed)
hist_others.SetLineColor(ROOT.kGreen+2)

# Canvas para todos os histogramas juntos
canvas = ROOT.TCanvas("canvas", "Deposicao de Energia Total por Particula", 800, 600)
hist_muon.Draw("HIST")
hist_pion.Draw("HIST SAME")
hist_others.Draw("HIST SAME")

# Legenda
legend = ROOT.TLegend(0.65, 0.7, 0.88, 0.88)
legend.AddEntry(hist_muon, "Muões (PDG 13)", "l")
legend.AddEntry(hist_pion, "Piões (PDG 211)", "l")
legend.AddEntry(hist_others, "Outras Partículas", "l")
legend.Draw()

canvas.Update()

# Manter a aplicação aberta
input("Pressione Enter para fechar...")

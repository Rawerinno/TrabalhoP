import ROOT

# Abrir ficheiro ROOT
file = ROOT.TFile("AmberTarget_Run_0.root")
tree = file.Get("hadronicVertex")

# Verificar se a árvore foi carregada
if not tree:
    raise RuntimeError("A árvore 'hadronicVertex' não foi encontrada.")

# Criar histogramas para primários e secundários
hist_primary = ROOT.TH1F("hist_primary", "Vertices Hadronicos vs Z;Z (cm);Contagem", 200, -50, 1000)
hist_secondary = ROOT.TH1F("hist_secondary", "", 200, -50, 1000)

# Preencher histogramas
tree.Draw("vertexPosZ_cm >> hist_primary", "IsPrimary == 1", "goff")
tree.Draw("vertexPosZ_cm >> hist_secondary", "IsPrimary == 0", "goff")

# Estilização
hist_primary.SetLineColor(ROOT.kBlue)
hist_secondary.SetLineColor(ROOT.kRed)

# Canvas
canvas = ROOT.TCanvas("canvas", "Vertices Hadronicos Primarios e Secundarios", 800, 600)
hist_primary.Draw("HIST")
hist_secondary.Draw("HIST SAME")

# Legenda
legend = ROOT.TLegend(0.65, 0.75, 0.88, 0.88)
legend.AddEntry(hist_primary, "Primários (IsPrimary == 1)", "l")
legend.AddEntry(hist_secondary, "Secundários (IsPrimary == 0)", "l")
legend.Draw()

canvas.Update()
input("Pressione Enter para sair...")

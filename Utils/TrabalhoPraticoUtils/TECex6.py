import ROOT

# Abrir ficheiro ROOT
file = ROOT.TFile("AmberTarget_Run_0.root")
tree = file.Get("Hits")

# Criar histogramas 2D para X vs Y
hist_primary = ROOT.TH2F("hist_primary", "Distribuição XY - Hits Primários;X (cm);Y (cm)", 100, -50, 50, 100, -50, 50)
hist_secondary = ROOT.TH2F("hist_secondary", "Distribuição XY - Hits Secundários;X (cm);Y (cm)", 100, -50, 50, 100, -50, 50)

# Preencher histogramas
tree.Draw("hitPosY_cm:hitPosX_cm >> hist_primary", "IsPrimary == 1", "goff")
tree.Draw("hitPosY_cm:hitPosX_cm >> hist_secondary", "IsPrimary == 0", "goff")

# Canvas com dois painéis
canvas = ROOT.TCanvas("canvas", "Distribuição XY de Hits", 1200, 600)
canvas.Divide(2, 1)

canvas.cd(1)
hist_primary.SetStats(0)
hist_primary.Draw("COLZ")

canvas.cd(2)
hist_secondary.SetStats(0)
hist_secondary.Draw("COLZ")

canvas.Update()
input("Pressione Enter para sair...")
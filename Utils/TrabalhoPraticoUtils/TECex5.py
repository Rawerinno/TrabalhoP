import ROOT

# Abrir ficheiro ROOT
file = ROOT.TFile("AmberTarget_Run_0.root")
tree = file.Get("Hits")

# Lista de detectores
detectors = [0, 1, 2, 3]

# Canvas dividido
canvas = ROOT.TCanvas("canvas", "Distribuição XY por Detetor", 1200, 800)
canvas.Divide(2, 2)

# Criar e desenhar histogramas
for i, det in enumerate(detectors):
    hist_name = f"hist_det{det}"
    hist_title = f"Distribuição XY - Detetor {det};X (cm);Y (cm)"
    
    hist = ROOT.TH2F(hist_name, hist_title, 100, -50, 50, 100, -50, 50)

    draw_expr = f"hitPosY_cm:hitPosX_cm >> {hist_name}"
    selection_expr = f"detectorID == {det}"
    tree.Draw(draw_expr, selection_expr, "goff")

    canvas.cd(i+1)
    hist.SetStats(0)
    hist.Draw("COLZ")

canvas.Update()
input("Pressione Enter para sair...")

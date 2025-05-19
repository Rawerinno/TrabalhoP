import ROOT;

file = ROOT.TFile.Open("AmberTarget_Run_0.root")
tree = file.Get("Hits")

# Criar histograma
hist = ROOT.TH1F("hist", "Distribuição temporal dos hits;Tempo [ns];Contagem", 100, 0, 10)

# Filtrar por um detetor específico (ex: detetor 3)
tree.Draw("particleHitTime_ns >> hist", "detectorID == 3")

# Mostrar
canvas = ROOT.TCanvas()
hist.Draw()
#canvas.SaveAs("histograma_hits_temporais.png")

input("Pressione Enter para sair...")

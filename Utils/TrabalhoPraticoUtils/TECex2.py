import ROOT

# Abrir ficheiro ROOT e obter a árvore
file = ROOT.TFile("AmberTarget_Run_0.root")
tree = file.Get("tracksData")

# Verificar se a árvore foi carregada corretamente
if not tree:
    raise RuntimeError("Não foi possível carregar a árvore 'tracksData'.")

# Criar histogramas
hist_muon_det0 = ROOT.TH1F("hist_muon_det0", "Deposicao de Energia - Muões no Detetor 0;Energia (keV);Contagem", 100, 0, 500)
hist_pion_det1 = ROOT.TH1F("hist_pion_det1", "Deposicao de Energia - Piões no Detetor 1;Energia (keV);Contagem", 100, 0, 500)
hist_others_det2 = ROOT.TH1F("hist_others_det2", "Deposicao de Energia - Outras Partículas no Detetor 2;Energia (keV);Contagem", 100, 0, 500)

# Preencher histogramas usando cortes baseados em particlePDG
tree.Draw("EdepDet0_keV >> hist_muon_det0", "particlePDG == 13")      # Muões
tree.Draw("EdepDet1_keV >> hist_pion_det1", "particlePDG == 211")     # Piões
tree.Draw("EdepDet2_keV >> hist_others_det2", "particlePDG != 13 && particlePDG != 211")  # Outras

# Estilo dos histogramas
hist_muon_det0.SetLineColor(ROOT.kBlue)
hist_pion_det1.SetLineColor(ROOT.kRed)
hist_others_det2.SetLineColor(ROOT.kGreen + 2)

# Canvas individual para cada histograma (ou unificado com pads, se preferir)
c1 = ROOT.TCanvas("c1", "Deposicao de Energia", 1200, 400)
c1.Divide(3, 1)  # 3 colunas

c1.cd(1)
hist_muon_det0.Draw()

c1.cd(2)
hist_pion_det1.Draw()

c1.cd(3)
hist_others_det2.Draw()

# Atualizar e manter as janelas abertas
c1.Update()
input("Pressione Enter para fechar...")

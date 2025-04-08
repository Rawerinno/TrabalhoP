
import ROOT

# Abrir o arquivo ROOT
file = ROOT.TFile("/home/cotton/Utils/TrabalhoPraticoUtils/AmberTarget_Run_0.root", "READ")

tree = file.Get("edep_Per_Event")  # Substitua pelo nome correto da árvore

# Criar histograma para cada detector
hist0 = ROOT.TH1F("hist0", "Deposicao de Energia - Detector 0", 500, 0, 500000)  # Ajuste os bins e range conforme necessário
hist1 = ROOT.TH1F("hist1", "Deposicao de Energia - Detector 1", 500, 0, 500000)
hist2 = ROOT.TH1F("hist2", "Deposicao de Energia - Detector 2", 500, 0, 500000)
hist3 = ROOT.TH1F("hist3", "Deposicao de Energia - Detector 3", 500, 0, 500000)

# Preencher os histogramas aplicando um corte para eventos válidos (eventID > 0)
tree.Draw("detector0 >> hist0", "eventID > 0")
tree.Draw("detector1 >> hist1", "eventID > 0")
tree.Draw("detector2 >> hist2", "eventID > 0")
tree.Draw("detector3 >> hist3", "eventID > 0")

# Criar um canvas para desenhar os histogramas
canvas = ROOT.TCanvas("canvas", "Deposicao de Energia", 800, 600)
canvas.Divide(2, 2)  # Criar uma grade 2x2 para os histogramas

canvas.cd(1)
hist0.Draw()
canvas.cd(2)
hist1.Draw()
canvas.cd(3)
hist2.Draw()
canvas.cd(4)
hist3.Draw()

canvas.Update()
canvas.Draw()

# Manter a aplicação aberta para visualizar os gráficos
input("Pressione Enter para sair...")



import ROOT
import multiprocessing

def histogramas(ficheiro):
    # Abrir o arquivo ROOT
    file = ROOT.TFile("AmberTarget_Run_"+str(ficheiro)+".root")  # Substitua pelo nome do seu arquivo ROOT
    tree = file.Get("edep_Per_Event")  # Substitua pelo nome correto da árvore

    # Criar histogramas para cada detector
    hist0 = ROOT.TH1F("hist0", "Deposicao de Energia - Todos os Detectores", 500, 0, 500000)
    hist1 = ROOT.TH1F("hist1", "", 500, 0, 500000)
    hist2 = ROOT.TH1F("hist2", "", 500, 0, 500000)
    hist3 = ROOT.TH1F("hist3", "", 500, 0, 500000)

    # Criar um canvas para desenhar os histogramas
    canvas = ROOT.TCanvas("canvas", "Deposicao de Energia", 800, 600)

    # Preencher os histogramas aplicando um corte para eventos válidos (eventID > 0)
    tree.Draw("detector0 >> hist0", "eventID > 0")
    tree.Draw("detector1 >> hist1", "eventID > 0")
    tree.Draw("detector2 >> hist2", "eventID > 0")
    tree.Draw("detector3 >> hist3", "eventID > 0")

    # Configurar estilos
    hist0.SetLineColor(ROOT.kRed)
    hist1.SetLineColor(ROOT.kBlue)
    hist2.SetLineColor(ROOT.kGreen)
    hist3.SetLineColor(ROOT.kMagenta)

    hist0.Draw("HIST")  # Desenhar o primeiro histograma
    hist1.Draw("HIST SAME")  # Sobrepor os demais
    hist2.Draw("HIST SAME")
    hist3.Draw("HIST SAME")

    # Configurar limite do eixo Y
    hist0.GetYaxis().SetRangeUser(0, 100)

    # Criar legenda
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(hist0, "Detector 0", "l")
    legend.AddEntry(hist1, "Detector 1", "l")
    legend.AddEntry(hist2, "Detector 2", "l")
    legend.AddEntry(hist3, "Detector 3", "l")
    legend.Draw()

    canvas.Update()
    canvas.Draw()
    canvas.SaveAs(f"ex01_Ficheiro_0{ficheiro}.png")

    # Manter a aplicação aberta para visualizar o gráfico
    #input("Pressione Enter para sair...")
    return

if __name__ == '__main__':
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()

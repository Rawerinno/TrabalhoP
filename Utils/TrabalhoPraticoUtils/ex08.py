import ROOT
import multiprocessing

def histogramas(ficheiro):
    # Abrir ficheiro ROOT e árvore
    file = ROOT.TFile.Open("AmberTarget_Run_"+str(ficheiro)+".root")
    tree = file.Get("Hits")

    # Criar histogramas
    h_muon = ROOT.TH1F("h_muon", "pZ dos muoes e pioes; pZ [GeV]; Contagem (log)", 3000, 0, 210)
    h_pion = ROOT.TH1F("h_pion", "", 3000, 0, 210)

    # Preencher histogramas com cortes
    tree.Draw("pZ_GeV >> h_muon", "abs(particlePDG) == 13", "goff")
    tree.Draw("pZ_GeV >> h_pion", "abs(particlePDG) == 211", "goff")

    # Rebin para suavizar (junta 5 bins em 1)
    h_muon.Rebin(5)
    h_pion.Rebin(5)

    # Estilo mais suave
    h_muon.SetLineColor(ROOT.kGreen+2)
    h_pion.SetLineColor(ROOT.kOrange+7)
    h_muon.SetLineWidth(2)
    h_pion.SetLineWidth(2)


    # Estilo
    h_muon.SetLineColor(ROOT.kBlue)
    h_pion.SetLineColor(ROOT.kRed)
    h_muon.SetLineWidth(2)
    h_pion.SetLineWidth(2)

    # Criar canvas com escala logarítmica no eixo Y
    c = ROOT.TCanvas("c", "pZ Muoes vs Pioes", 800, 600)
    c.SetLogy()

    # Definir limites Y (opcional, para melhor visualização)
    h_muon.GetYaxis().SetRangeUser(1, 1e4)

    # Desenhar
    h_muon.Draw("HIST")
    h_pion.Draw("HIST SAME")

    # Legenda
    legend = ROOT.TLegend(0.65, 0.75, 0.88, 0.88)
    legend.AddEntry(h_muon, "Muoes", "l")
    legend.AddEntry(h_pion, "Pioes", "l")
    legend.Draw()

    c.Update()
    c.SaveAs(f"ex08_Ficheiro_0{ficheiro}.png")



if __name__ == '__main__':
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
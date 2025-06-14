import ROOT
import multiprocessing

def histogramas(ficheiro):
    # Abrir ficheiro e árvore
    file = ROOT.TFile.Open("AmberTarget_Run_"+str(ficheiro)+".root")
    tree = file.Get("Hits")

    # Criar histogramas
    h_prim = ROOT.TH1F("h_prim", "pZ dos pioes primarios e secundarios; pZ [GeV]; Contagem (log)", 1000, 0, 210)
    h_sec = ROOT.TH1F("h_sec", "", 1000, 0, 210)

    # Preencher
    tree.Draw("pZ_GeV >> h_prim", "abs(particlePDG) == 211 && IsPrimary == 1", "goff")
    tree.Draw("pZ_GeV >> h_sec", "abs(particlePDG) == 211 && IsPrimary == 0", "goff")

    # Rebin para suavizar (junta 5 bins em 1)
    h_prim.Rebin(5)
    h_sec.Rebin(5)

    # Estilo mais suave
    h_prim.SetLineColor(ROOT.kGreen+2)
    h_sec.SetLineColor(ROOT.kOrange+7)
    h_prim.SetLineWidth(2)
    h_sec.SetLineWidth(2)

    # Canvas com escala log
    c = ROOT.TCanvas("c", "pZ pioes primarios e secundarios", 800, 600)
    c.SetLogy()

    # Definir limites
    h_prim.GetYaxis().SetRangeUser(1, 1e5)
    h_prim.GetXaxis().SetRangeUser(0, 250)

    # Desenhar
    h_prim.Draw("HIST")
    h_sec.Draw("HIST SAME")

    # Legenda
    legend = ROOT.TLegend(0.65, 0.75, 0.88, 0.88)
    legend.AddEntry(h_prim, "Pioes primarios", "l")
    legend.AddEntry(h_sec, "Pioes secundarios", "l")
    legend.Draw()

    c.Update()
    c.SaveAs(f"ex09_Ficheiro_0{ficheiro}.png")



if __name__ == '__main__':
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
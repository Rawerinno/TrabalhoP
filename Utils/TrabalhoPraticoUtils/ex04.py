import ROOT
import multiprocessing

def histogramas(ficheiro):
    # Abrir ficheiro ROOT
    file = ROOT.TFile("AmberTarget_Run_"+str(ficheiro)+".root")
    tree = file.Get("hadronicVertex")

    # Histogramas com mais bins
    hist_primary   = ROOT.TH1F("hist_primary",   "Vertices Hadronicos vs Z;Z (cm);Contagem (log)", 400, -50, 600)
    hist_secondary = ROOT.TH1F("hist_secondary", "",                                     400, -50, 600)

    # Preencher
    tree.Draw("vertexPosZ_cm >> hist_primary",   "IsPrimary == 1", "goff")
    tree.Draw("vertexPosZ_cm >> hist_secondary", "IsPrimary == 0", "goff")

    # Estilização
    hist_primary.SetLineColor(ROOT.kBlue)
    hist_primary.SetLineWidth(2)
    hist_secondary.SetLineColor(ROOT.kRed)
    hist_secondary.SetLineWidth(2)

    # Ajuste de títulos e tamanhos de fonte
    for h in (hist_primary, hist_secondary):
        h.GetXaxis().SetTitle("Z (cm)")
        h.GetXaxis().SetTitleSize(0.05)
        h.GetXaxis().SetLabelSize(0.04)
        h.GetYaxis().SetTitle("Contagem")
        h.GetYaxis().SetTitleSize(0.05)
        h.GetYaxis().SetLabelSize(0.04)
        h.GetYaxis().SetTitleOffset(1.3)

    # Ajuste de limites dos eixos
    # Define intervalo X de 0 a 800 cm
    hist_primary.GetXaxis().SetRangeUser(0, 600)
    hist_secondary.GetXaxis().SetRangeUser(0, 600)
    # Para escala log: mínimo e máximo do Y
    hist_primary.SetMinimum(0.1)
    hist_secondary.SetMinimum(0.1)
    # Também podes definir um máximo (ex.: 1e2)
    hist_primary.SetMaximum(1e2)
    hist_secondary.SetMaximum(1e2)

    # Canvas com escala log no Y
    canvas = ROOT.TCanvas("canvas", "Vertices Hadronicos Primarios e Secundarios", 800, 600)
    canvas.SetLogy()

    # Desenhar
    hist_primary.Draw("HIST")
    hist_secondary.Draw("HIST SAME")

    # Legenda
    legend = ROOT.TLegend(0.65, 0.75, 0.88, 0.88)
    legend.AddEntry(hist_primary,   "Primarios (IsPrimary == 1)", "l")
    legend.AddEntry(hist_secondary, "Secundarios (IsPrimary == 0)", "l")
    legend.Draw()

    canvas.Update()
    canvas.SaveAs(f"ex04_Ficheiro_0{ficheiro}.png")


if __name__ == '__main__':
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
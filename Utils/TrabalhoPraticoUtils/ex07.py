import ROOT
import multiprocessing

def histogramas(ficheiro):
    # 1) Abre o ficheiro e acede à árvore Hits
    file = ROOT.TFile.Open("AmberTarget_Run_"+str(ficheiro)+".root")
    tree = file.Get("Hits")

    # 2) Lista de detectores
    detectors = [0, 1, 2, 3]

    # 3) Cria um canvas dividido em 2x2 pads
    canvas = ROOT.TCanvas("canvas_time", "Distribuicao Temporal dos Hits por Detector", 1200, 1000)
    canvas.Divide(2, 2)

    # 4) Para cada detector, cria e preenche um histograma de tempos
    histos = {}
    for i, det in enumerate(detectors):
        canvas.cd(i+1)
        ROOT.gPad.SetLogy()                # escala logarítmica no eixo Y deste pad

        hname = f"hist_time_det{det}"
        title = f"Detector {det} – Tempo dos Hits;Tempo [ns];Contagem"
        hist = ROOT.TH1F(hname, title, 100, 2, 18000)   # 100 bins de 0 a 10 ns
        hist.SetLineWidth(2)
        hist.SetLineColor(ROOT.kBlue + i)
        hist.SetMinimum(1)                 # mínimo para log

        # Preenche só com hits do detector atual
        cut = f"detectorID == {det}"
        tree.Draw(f"particleHitTime_ns >> {hname}", cut, "goff")

        # Desenha o histograma
        hist.Draw("HIST")
        histos[det] = hist

    # 5) Atualiza o canvas
    canvas.Update()
    canvas.SaveAs(f"ex07_Ficheiro_0{ficheiro}.png")


if __name__ == '__main__':
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
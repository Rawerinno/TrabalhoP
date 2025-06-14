import ROOT
import multiprocessing

def histogramas(ficheiro):
    # Abrir ficheiro ROOT
    file = ROOT.TFile("AmberTarget_Run_"+str(ficheiro)+".root")
    tree = file.Get("Hits")

    # Lista de detectores
    detectors = [0, 1, 2, 3]

    # Canvas dividido em 2x2
    canvas = ROOT.TCanvas("canvas", "Distribuicao XY por Detetor", 1200, 800)
    canvas.Divide(2, 2)

    # Lista para manter histogramas vivos (evita serem apagados do gDirectory)
    hist_list = []

    for i, det in enumerate(detectors):
        hist_name = f"hist_det{det}"
        hist_title = f"Distribuicao XY - Detetor {det};X (cm);Y (cm)"

        # Criar histograma diretamente
        hist = ROOT.TH2F(hist_name, hist_title, 200, -45, 45, 100, -45, 45)

        # Preencher com tree.Project (evita conflito com gDirectory)
        cut = f"detectorID == {det}"
        tree.Project(hist_name, "hitPosY_cm:hitPosX_cm", cut, "goff")

        # Guardar histograma para manter em memória
        hist_list.append(hist)

        # Desenhar no pad correspondente
        canvas.cd(i + 1)
        hist.SetStats(0)
        hist.Draw("COLZ")

    canvas.Update()
    canvas.SaveAs(f"ex05_Ficheiro_0{ficheiro}.png")


if __name__ == '__main__':
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
import ROOT
import multiprocessing

def histogramas(ficheiro):
    # 1) Abre o ficheiro e acede à árvore Hits
    f    = ROOT.TFile("AmberTarget_Run_"+str(ficheiro)+".root")
    tree = f.Get("Hits")

    # 2) Lista de detectores e categorias
    detectors  = [0, 1, 2, 3]
    categories = ["charged", "neutral"]

    # 3) Configuração do canvas 2 colunas (categoria) x 4 linhas (detetores)
    canvas = ROOT.TCanvas("canvas2", "Distribuicao XY por Detetor e Tipo", 1600, 2000)
    canvas.Divide(2, 4)

    # 4) Manter histos vivos
    hist_list = []

    # 5) Loop sobre detectores e categorias
    for i, det in enumerate(detectors):
        for j, cat in enumerate(categories):
            pad_index = i*2 + j + 1
            canvas.cd(pad_index)
            
            # Cria TH2F
            hist_name  = f"hist_{cat}_det{det}"
            hist_title = f"Detetor {det} - {cat.capitalize()};X (cm);Y (cm)"
            hist = ROOT.TH2F(hist_name, hist_title, 200, -45, 45, 100, -45, 45)
            hist.SetStats(0)
            
            # Define corte por categoria
            if cat == "charged":
                cut = f"detectorID=={det} && !(abs(particlePDG)==22 || abs(particlePDG)==2112)"
            else:
                cut = f"detectorID=={det} && (abs(particlePDG)==22 || abs(particlePDG)==2112)"
            
            # Preencher
            tree.Project(hist_name, "hitPosY_cm:hitPosX_cm", cut, "goff")
            
            # Desenhar
            hist.Draw("COLZ")
            hist_list.append(hist)

    canvas.Update()
    canvas.SaveAs(f"ex06_Ficheiro_0{ficheiro}.png")


if __name__ == '__main__':
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
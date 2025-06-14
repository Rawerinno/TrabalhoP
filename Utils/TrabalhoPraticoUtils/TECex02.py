import ROOT
import multiprocessing

def histogramas(ficheiro):
    # 1) Abre o ficheiro e acede à árvore Hits
    f   = ROOT.TFile(f"AmberTarget_Run_{ficheiro}.root")
    hit = f.Get("Hits")

    # 2) Detectores
    detectors = [0,1,2,3]

    # 3) Define categorias com PDG conjugados juntos e outras partículas
    categories = {
        "muons":     [13, -13],
        "pions":     [211, -211],
        "electrons": [11, -11],
        "gamma":     [22],
        "protons":   [2212],
    }

    # 4) Cores para cada categoria
    color_list = [
        ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta,
        ROOT.kCyan, ROOT.kOrange, ROOT.kBlack
    ]
    colors = {cat: color_list[i % len(color_list)] for i, cat in enumerate(categories)}

    # 5) Cria histogramas: um por (detector, categoria)
    histos = {}
    for det in detectors:
        for cat in categories:
            hname = f"h_{cat}_det{det}"
            title = f"Edep de {cat} no detector {det}"
            h = ROOT.TH1F(hname, title, 200, 0, 10000)
            h.SetLineWidth(2)
            h.SetLineColor(colors[cat])
            histos[(det, cat)] = h

    # 6) Loop manual sobre todas as entradas e preenchimento
    n_entries = hit.GetEntries()
    for i in range(n_entries):
        hit.GetEntry(i)
        detID = int(hit.detectorID)
        pdg   = int(hit.particlePDG)
        edep  = hit.Edep_keV
        if detID not in detectors:
            continue
        for cat, pdg_list in categories.items():
            if pdg in pdg_list:
                histos[(detID, cat)].Fill(edep)
                break

    # 7) Ajusta limites de Y em cada detector para acomodar o máximo
    y_max = {}
    for det in detectors:
        peak = max(histos[(det,cat)].GetMaximum() for cat in categories)
        y_max[det] = peak * 1.2

    # 8) Desenha tudo num único canvas 2×2 em escala logarítmica no Y
    canvas = ROOT.TCanvas("canvas_all", "Deposição por categoria e detector", 1200, 1200)
    canvas.Divide(2, 2)

    for i, det in enumerate(detectors):
        canvas.cd(i+1)
        ROOT.gPad.SetLogy(1)     # ativa log-Y neste pad
        first = True
        for cat in categories:
            h = histos[(det, cat)]
            h.GetXaxis().SetTitle("Edep [keV]")
            h.GetYaxis().SetTitle("Contagem")
            h.GetXaxis().SetRangeUser(0, 10000)
            h.GetYaxis().SetRangeUser(1, y_max[det])  # mínimo ≥1
            opt = "HIST" if first else "HIST SAME"
            h.Draw(opt)
            first = False

        # legenda
        leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
        for cat in categories:
            leg.AddEntry(histos[(det,cat)], cat.capitalize(), "l")
        leg.Draw()

    # 9) Salva a figura e fecha
    canvas.Modified()
    canvas.Update()
    canvas.SaveAs(f"ex02_Ficheiro_0{ficheiro}.png")
    canvas.Close()
    f.Close()


if __name__ == "__main__":
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
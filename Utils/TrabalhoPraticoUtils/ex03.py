import ROOT
import multiprocessing

def histogramas(ficheiro):
    # 1) Abre o ficheiro e acede à árvore Hits
    f   = ROOT.TFile("AmberTarget_Run_"+str(ficheiro)+".root")
    hit = f.Get("Hits")

    # 2) Define categorias com PDG conjugados juntos e outras partículas
    categories = {
        "muons":     [13, -13],   # mu- e mu+
        "pions":     [211, -211], # pi+ e pi-
        "electrons": [11, -11],   # e- e e+
        "gamma":     [22],        # fotão
        "protons":   [2212],      # protão
    }

    # 3) Cores para cada categoria
    color_list = [
        ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta,
        ROOT.kCyan, ROOT.kOrange, ROOT.kBlack, ROOT.kViolet
    ]
    colors = {cat: color_list[i % len(color_list)] for i, cat in enumerate(categories)}

    # 4) Acumula Edep_keV total por evento e categoria (soma sobre os 4 detectores)
    totals = {}  # chave: (eventID, categoria) -> soma de Edep_keV
    n_entries = hit.GetEntries()
    for i in range(n_entries):
        hit.GetEntry(i)
        pdg = int(hit.particlePDG)
        evt = int(hit.eventID)
        for cat, pdg_list in categories.items():
            if pdg in pdg_list:
                key = (evt, cat)
                totals[key] = totals.get(key, 0.0) + hit.Edep_keV
                break

    # 5) Cria um histograma para cada categoria
    histos = {}
    for cat in categories:
        h = ROOT.TH1F(
            f"h_tot_{cat}",
            f"Soma total de energia - {cat}",
            100, 0, 10000  # 200 bins de 0 a 5000 keV
        )
        h.SetLineWidth(2)
        histos[cat] = h

    # 6) Preenche cada histograma: uma entrada por evento
    for (evt, cat), sum_edep in totals.items():
        histos[cat].Fill(sum_edep)

    # 7) Desenha todos os histogramas sobrepostos num único canvas
    c = ROOT.TCanvas("c_tot_all", "Perda total de energia por categoria", 900, 600)
    c.SetLogy()  # escala logarítmica no eixo Y

    first = True
    for cat, h in histos.items():
        h.SetLineColor(colors[cat])
        h.GetXaxis().SetTitle("Energia total depositada [keV]")
        h.GetYaxis().SetTitle("Número de eventos")
        opt = "HIST" if first else "HIST SAME"
        h.Draw(opt)
        first = False

    # 8) Legenda
    leg = ROOT.TLegend(0.65, 0.65, 0.9, 0.9)
    for cat in histos:
        leg.AddEntry(histos[cat], cat.capitalize(), "l")
    leg.Draw()

    c.Update()
    c.SaveAs(f"ex03_Ficheiro_0{ficheiro}.png")


if __name__ == '__main__':
    ficheiros = [0, 1, 2, 3]
    processos = []

    for ficheiro in ficheiros:
        p = multiprocessing.Process(target=histogramas, args=(ficheiro,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
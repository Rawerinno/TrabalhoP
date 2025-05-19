void ReadFile(){

TFile *ficheiro = new TFile("teste.root","READ");
TTree *dados=(TTree*)ficheiro->Get("eventos");

Int_t Nep;
Int_t Nep_2;
dados->SetBranchAddress("Nep",&Nep);

Long64_t nEntries=dados->GetEntries();

cout<<nEntries<<endl;

TFile *newFile=new TFile("novoFicheiro.root","RECREATE");

TTree *newTree =new TTree ("novaTree","nova arvore");
newTree->Branch("Nep",&Nep_2,"Nep/I");

for (Int_t i=0;i<nEntries;i++){

    dados->GetEntry(i);
    Nep_2=2*Nep;
    newTree->Fill();

}



//Int_t nBins=500;
Int_t minBin=dados->GetMinimum("Nep");
Int_t maxBin=dados->GetMaximum("Nep");
Int_t nBins=maxBin-minBin;

TH1I *hNep=new TH1I("hNep","hNep",nBins,minBin,maxBin);

Int_t nBinsX=500;
Double_t maxX=dados->GetMaximum("mediaX");
Double_t minX=dados->GetMinimum("mediaX");
Int_t nBinsY=500;
Double_t maxY=dados->GetMaximum("mediaY");
Double_t minY=dados->GetMinimum("mediaY");


TH2D *histoPos=new TH2D("histoPos","histoPos",nBinsX,minX,maxX,nBinsX,minY,maxY);


dados->Draw("Nep>>hNep","","goff");//goff não desenha histograma
hNep->GetXaxis()->SetTitle("NEP");
hNep->SetFillColor(kRed);
hNep->Draw("BAR");

TCanvas *newCanvas=new TCanvas("newCanvas","newCanvas");
dados->Draw("mediaY:mediaX>>histoPos","","goff");
histoPos->Draw("COLZ");


newTree->Write();



}

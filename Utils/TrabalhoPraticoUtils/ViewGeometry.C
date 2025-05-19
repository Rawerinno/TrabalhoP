void ViewGeometry()
{
	gSystem->Load("libGeom");
	gSystem->Load("libGdml");
	TGeoManager *geom = new TGeoManager();
	TGeoChecker *checker = new TGeoChecker(geom);
	geom->SetNsegments(4); // Doesn't matter keep low
	
	geom->Import("AmberTarget.gdml");

	geom->SetCheckingOverlaps(true);

	//int colors[9] =
	//{ kBlack, kYellow, kGray, kBlue, kOrange, kGreen, kRed, kCyan, kMagenta};
	//double transparency[9] =
	//{ 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,0.5 };


	//geom->CheckGeometryFull();





	TObjArray *volumes = geom->GetListOfVolumes();
	TIter nextV(volumes);
	TGeoVolume *vol;
	TString volName;
	int z = 0;
	while ((vol = (TGeoVolume*) nextV()))
	{
			volName=vol->GetName();
		if (volName=="detectorLogical"){
				vol->SetTransparency(50);	
			}
			
		//sourceLogical is hard to Draw in GMDL, use X3D intead to view	
		if (volName=="sourceLogical"){
			vol->SetTransparency(80); 	
			}	


			cout<<volName<<endl;
	}
	geom->PrintOverlaps();
	

	geom->GetTopVolume()->Draw("ogl");


}

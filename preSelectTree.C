
const int nmultMax = 40223;
void preSelectTree(){
    
    TFile *file = new TFile("/storage1/users/wl33/AMPT/ampttree_PbPb_r0.root");

    
    TTreeReader theReader("ampttree_particles",file);    
    TTreeReaderValue<Int_t> nmult(theReader, "nmult");
    TTreeReaderArray<Float_t> px(theReader, "px");
    TTreeReaderArray<Float_t> py(theReader, "py");
    TTreeReaderArray<Float_t> pz(theReader, "pz"); 
    TTreeReaderArray<Int_t>   pid(theReader, "pid");     
    TTreeReaderValue<Float_t> b(theReader, "b");
    
    
    TFile *fileOut = new TFile("./preSelectedData.root","RECREATE");
    TTree *treeOut = new TTree("ampttree_particles", "preselected data");
    TTree::SetBranchStyle(0);
    Int_t nmult_ = 0;
    Float_t pt_[nmultMax];
	Float_t b_ = 0.;
    Float_t eta_[nmultMax];
    Float_t phi_[nmultMax];
    Int_t pid_[nmultMax];
    treeOut->Branch("nmult",&nmult_, "nmult/I");
    treeOut->Branch("pt",pt_, "pt[nmult]/F");
	treeOut->Branch("b",&b_, "b/F");
    treeOut->Branch("eta",eta_, "eta[nmult]/F");
    treeOut->Branch("phi",phi_, "phi[nmult]/F");
    treeOut->Branch("pid",pid_, "pid[nmult]/I");
    
    int evtNr = 0;
    int j=0;
    while(theReader.Next()){
        evtNr++;
        if(evtNr%100==0)cout << evtNr << endl;
       // if(evtNr%1000==0)break;
        j=0;
		sum_pt=0;
		b_ = *b;
        for(int i=0;i<*nmult;i++){
            
            eta_[j] = -log(tan(atan(sqrt(pow(px[i],2)+pow(py[i],2))/fabs(pz[i]))/2))*(pz[i]/fabs(pz[i]));
            if(fabs(eta_[j])>5)continue;
            
            pid_[j] = pid[i];
            if(pid_[j]>15000||pid_[j]<-5000)continue;
            
			
            pt_[j]=sqrt(px[i]*px[i]+py[i]*py[i]);
			
			sum_pt=sum_pt+pt_[j];
        
            if(px[i]==0) phi_[j]=-4;
            if(px[i]==0&&py[i]!=0) phi_[j]=py[i]/fabs(py[i])*TMath::Pi()/2;
            else phi_[j] = atan(py[i]/px[i])+(px[i]<=0)*(TMath::Pi()-2*(py[i]<=0)*TMath::Pi());
            
            
            j+=1;
        }
        nmult_ = j;
		if(j>0 && sum_pt>0.2)treeOut->Fill();
            
    }
    
  fileOut->Write();
  
  
 TCanvas* c = new TCanvas("c","c");
 c->Divide(2,2);
 
 c->cd(1);
 treeOut->Draw("phi>>hist1(1000,-1,1)");
 c->cd(2);
 treeOut->Draw("pt>>hist(200,0,3)");
 c->cd(3);
 treeOut->Draw("eta");
 c->cd(4);
 treeOut->Draw("b");
 
 
 c->Print("phi.png"); 
  
}

import ROOT

import os
from array import array

from DevTools.Plotter.xsec import getXsec
from DevTools.Plotter.utilities import getLumi, isData, hashFile, hashString, python_mkdir, getTreeName, getNtupleDirectory, getSkimJson, getSkimPickle
from DevTools.Plotter.Plotter import Plotter
import DevTools.Plotter.CMS_lumi as CMS_lumi

outputLog=open('test.log','w')

of=ROOT.TFile('output.root','RECREATE')
dataTree=ROOT.TTree('ThreePhotonTree_Data','Three photon tree')
mcTree=ROOT.TTree('ThreePhotonTree_MC','Three photon tree')
ggg_mass_arr=array('f',[0.])
ggg_mass_weight_arr=array('f',[0.])
dataTree.Branch('m_ggg',ggg_mass_arr,'m_ggg/F')
dataTree.Branch('m_ggg_weight',ggg_mass_weight_arr,'m_ggg_weight/F')
mcTree.Branch('m_ggg',ggg_mass_arr,'m_ggg/F')
mcTree.Branch('m_ggg_weight',ggg_mass_weight_arr,'m_ggg_weight/F')

def setStyle(pad,position=11,preliminary=True,personal=True,period_int=4):
    '''Set style for plots based on the CMS TDR style guidelines.
       https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines#Figures_and_tables
       https://ghm.web.cern.ch/ghm/plots/'''
    # set period (used in CMS_lumi)
    # period : sqrts
    # 1 : 7, 2 : 8, 3 : 7+8, 4 : 13, ... 7 : 7+8+13
    # set position
    # 11: upper left, 33 upper right
    CMS_lumi.cmsText = 'CMS' if not personal else 'Christopher Brainerd'
    CMS_lumi.writeExtraText = preliminary if not personal else True
    CMS_lumi.extraText = "Preliminary" if not personal else 'Analysis in Progress'
    CMS_lumi.lumi_13TeV = "%0.1f fb^{-1}" % (float(getLumi())/1000.)
    if getLumi < 1000:
        CMS_lumi.lumi_13TeV = "%0.1f pb^{-1}" % (float(getLumi))
    CMS_lumi.CMS_lumi(pad,period_int,position)

crab_dir='/uscms_data/d3/cbrainer/crab_projects/ThreePhoton/2017-06-29_01:48:48'

analysis,date=crab_dir.split('/')[5:7]
print analysis
print date
datasets=[datasetDir for datasetDir in os.listdir(crab_dir) if os.path.isdir('/'.join((crab_dir,datasetDir)))]
luminosity=getLumi()
print luminosity

gCanvas=ROOT.TCanvas()
gCanvas.cd()
gTH1D=ROOT.TH1D('mc','mc',100,0,1000)
dTH1D=ROOT.TH1D('data','data',100,0,1000)

allDatasets='''
DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
DiPhotonJetsBox_M40_80-Sherpa
DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa
DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8
DoubleEG
DoubleMuon
SingleElectron
SinglePhoton
TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8
TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8
TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8
TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
WGGJets_TuneCUETP8M1_13TeV_madgraphMLM_pythia8
WGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8
WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8
WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8
ZGGJetsToLLGG_5f_LO_amcatnloMLM_pythia8
ZGGJets_ZToHadOrNu_5f_LO_madgraph_pythia8
ZGGToLLGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8
ZGGToNuNuGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8
ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
'''.split('\n')
    
def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(ROOT.kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0.8)
    h3.SetMaximum(1.35)
    # Set up plot
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)
    
    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio h1/h2 ")
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(15)
    
    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4.0)
    x.SetLabelFont(43)
    x.SetLabelSize(15)
    
    return h3

Datasets='''
DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8
DoubleEG
DoubleMuon
SingleElectron
SinglePhoton
TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8
TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8
TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8
TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
WGGJets_TuneCUETP8M1_13TeV_madgraphMLM_pythia8
WGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8
WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8
WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8
ZGGJetsToLLGG_5f_LO_amcatnloMLM_pythia8
ZGGJets_ZToHadOrNu_5f_LO_madgraph_pythia8
ZGGToLLGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8
ZGGToNuNuGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8
ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
'''.split('\n')

mcHists=dict((dataset,ROOT.TH1D(dataset,dataset,100,0,1000)) for dataset in Datasets if not isData(dataset))

for datasetDir in datasets:
    numberOfEvents=0
    ggg_mass=[]
    dataset='_'.join([x for x in datasetDir.split('_') if x not in '_'.join((analysis,date,'crab')).split('_')])
    if dataset not in Datasets:
        continue
    xsec=getXsec(dataset)
    isMC=not isData(dataset)
    thisHist=None
    if isMC:
        mcTree.Branch('_'.join(('m_ggg',dataset)),ggg_mass_arr,'_'.join(('m_ggg',dataset))+'/F')
        mcTree.Branch('_'.join(('m_ggg_weights',dataset)),ggg_mass_weight_arr,'_'.join(('m_ggg_weights',dataset))+'/F')
    resultsDir='/'.join((crab_dir,datasetDir,'results'))
    for fn in os.listdir(resultsDir):
        print 'Opening input file %s' % (fn)
        f=ROOT.TFile.Open('/'.join((resultsDir,fn)),'read')
        for event in f.ThreePhotonTree:
            ggg_mass.append(event.ggg_mass)
    numberOfEvents=len(ggg_mass)
    eventWeight=luminosity*xsec/numberOfEvents/1000 if isMC else 1 #???
    outputLog.write('%s\nEvents: %i\nWeight: %0.1f\n' % (dataset,numberOfEvents,eventWeight))
    for x in ggg_mass:
        ggg_mass_arr[0]=x
        ggg_mass_weight_arr[0]=eventWeight
        if isMC:
            gTH1D.Fill(x,eventWeight)
            mcHists[dataset].Fill(x,eventWeight)
            mcTree.Fill()
        else:
            dTH1D.Fill(x,1)
            dataTree.Fill()

#gTH1D.SetLineColor(2)
dTH1D.SetLineColor(4)
#gTH1D.Draw('HIST SAME')
dTH1D.Draw('HIST SAME')
ths=ROOT.THStack('MC','MC')
Colors=[ROOT.kBlue,ROOT.kSpring,ROOT.kTeal,ROOT.kMagenta,ROOT.kAzure,ROOT.kCyan,ROOT.kViolet,ROOT.kRed,ROOT.kOrange,ROOT.kPink,ROOT.kGreen,ROOT.kGray,ROOT.kWhite,ROOT.kBlack]
for number,x in enumerate(mcHists.values()):
    x.SetFillColor(Colors[number%len(Colors)])
    ths.Add(x)
ths.Draw('HIST SAME')
dTH1D.SetTitle('Data;m_{ggg} [GeV];Events per 10 GeV')
#setStyle(gCanvas)
gCanvas.BuildLegend()
gCanvas.SetLogy()

gCanvas.Print('output.pdf')
ratioPlot=createRatio(gTH1D,dTH1D)
ratio.Draw()
gCanvas.Print('ratio.pdf')


of.Write()
of.Close()

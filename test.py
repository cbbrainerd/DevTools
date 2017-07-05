import ROOT

import os
from array import array
import itertools

from DevTools.Plotter.xsec import getXsec
from DevTools.Plotter.utilities import getLumi, isData, hashFile, hashString, python_mkdir, getTreeName, getNtupleDirectory, getSkimJson, getSkimPickle
from DevTools.Plotter.Plotter import Plotter
import DevTools.Plotter.CMS_lumi as CMS_lumi

binSize=25
maxGeV=1000
minGeV=0

if((maxGeV-minGeV)%binSize):
    print 'Bin size should evenly divide range.'
    raise SystemExit
else:
    numBin=(maxGeV-minGeV)/binSize

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

def setStyle(pad,position=11,preliminary=True,personal=False,period_int=4):
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
gTH1D=ROOT.TH1D('mc','mc',numBin,minGeV,maxGeV)
dTH1D=ROOT.TH1D('data','data',numBin,minGeV,maxGeV)

DatasetDict= {
#    'DYJetsToLL_madgraphMLM' : [ 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' ],
    'DYJetsToLL_amcatnlo' : [ 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' , 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' ],
    'DiPhotonJetsBox_Sherpa' : [ 'DiPhotonJetsBox_M40_80-Sherpa' , 'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa' ],
#    'DiPhotonJets_amcatnlo' : [ 'DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8' ],
    'T+Jets' : [ 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 'TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' ],
    'T+G+Jets' : [ 'TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8' , 'TTGG_0Jets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8' , 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8' ],
    'W+Jets' : [ 'W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 'W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 'W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 'W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' ],
    'W/Z+G+Jets' : [ 'WGGJets_TuneCUETP8M1_13TeV_madgraphMLM_pythia8' , 'WGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8' , 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' , 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , 
'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8' ,'WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8' ,'ZGGJetsToLLGG_5f_LO_amcatnloMLM_pythia8' ,'ZGGJets_ZToHadOrNu_5f_LO_madgraph_pythia8' ,'ZGGToLLGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8' ,'ZGGToNuNuGG_5f_TuneCUETP8M1_13TeV-amcatnlo-pythia8' ,'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' ],
    'G+Jets' : [ 'GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8' , 'GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8' , 'GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8' ],
    'QCD' : ['QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8' , 'QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8' , 'QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8' ]
}

def createRatio(h1, h2,logFile=None):
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
    if logFile:
        nbins=x.GetNbins()
        for y in xrange(nbins):
            logFile.write('%i\n'%(h3.GetBinContent(y)))
    return h3

UnusedDatasets='''
DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
DiPhotonJetsBox_M40_80-Sherpa
DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa
'''.split('\n')

mcHists=dict()
mcHistList=[]
for histogram in DatasetDict.keys():
    tempHist=ROOT.TH1D(histogram,histogram,numBin,minGeV,maxGeV)
    mcHistList.append(tempHist)
    for dataset in DatasetDict[histogram]:
        mcHists[dataset]=tempHist

for datasetDir in datasets:
    numberOfEvents=0
    ggg_mass=[]
    ggg_weight=[]
    dataset='_'.join([x for x in datasetDir.split('_') if x not in '_'.join((analysis,date,'crab')).split('_')])
    if dataset in UnusedDatasets:
        continue
    xsec=getXsec(dataset)
    isMC=not isData(dataset)
    thisHist=None
    if isMC:
        mcTree.Branch('_'.join(('m_ggg',dataset)),ggg_mass_arr,'_'.join(('m_ggg',dataset))+'/F')
        mcTree.Branch('_'.join(('m_ggg_weights',dataset)),ggg_mass_weight_arr,'_'.join(('m_ggg_weights',dataset))+'/F')
    resultsDir='/'.join((crab_dir,datasetDir,'results'))
    numberOfEvents=0.
    for fn in os.listdir(resultsDir):
        print 'Opening input file %s' % (fn)
        f=ROOT.TFile.Open('/'.join((resultsDir,fn)),'read')
        numberOfEvents+=f.summedWeights.GetBinContent(1)
        for event in f.ThreePhotonTree:
            if (event.g1_mvaNonTrigValues > -.2 and event.g2_mvaNonTrigValues > -.2 and event.g3_mvaNonTrigValues > -.2):
                ggg_mass.append(event.ggg_mass)
                if isMC:
                    ggg_weight.append(event.genWeight*event.pileupWeight)
                else:
                    ggg_weight.append(1)
    if isMC:
        eventWeight=luminosity*xsec/float(numberOfEvents)
    else:
        eventWeight=1
    outputLog.write('%s\nEvents: %i\nWeight: %0.6f\n' % (dataset,numberOfEvents,eventWeight))
    for x,y in itertools.izip(ggg_mass,ggg_weight):
        ggg_mass_arr[0]=x
        ggg_mass_weight_arr[0]=eventWeight*y
        if isMC:
            gTH1D.Fill(x,eventWeight*y)
            mcHists[dataset].Fill(x,eventWeight*y)
            mcTree.Fill()
        else:
            dTH1D.Fill(x,1)
            dataTree.Fill()

#gTH1D.SetLineColor(2)
dTH1D.SetLineColor(4)
#gTH1D.Draw('HIST SAME')
ths=ROOT.THStack('MC','MC')
Colors=[ROOT.kRed,ROOT.kGreen,ROOT.kBlue]
mcHistList.sort(key=lambda x:x.GetEntries())
for x in mcHistList:
    try:
        outputLog.write('%s: %i\n' % (x.GetName(),mcHistList.GetEntries()))
    except:
        pass
for number,x in enumerate(mcHistList):
    x.SetFillColor(Colors[number%len(Colors)])
    ths.Add(x)
ths.Draw('HIST')
dTH1D.Draw('P SAME')
dTH1D.SetTitle('Data;m_{ggg} [GeV];Events per %i GeV' % binSize)
#setStyle(gCanvas)
gCanvas.BuildLegend()
gCanvas.SetLogy()

gCanvas.Print('output.pdf')
dTH1D.SetTitle('Data;;Events per %i GeV' % binSize)
ths.Draw('HIST')
dTH1D.Draw('P SAME')
canvasratio=0.3
gCanvas.SetBottomMargin(canvasratio + (1-canvasratio)*gCanvas.GetBottomMargin()-canvasratio*gCanvas.GetTopMargin())
ratioPad=ROOT.TPad('BottomPad','',0,0,1,1)
ratioPad.SetTopMargin((1-canvasratio) - (1-canvasratio)*ratioPad.GetBottomMargin()+canvasratio*ratioPad.GetTopMargin())

dTH1D.SetLabelOffset(999)
ratioPad.SetFillStyle(4000);
ratioPad.SetFillColor(4000);
ratioPad.SetFrameFillColor(4000);
ratioPad.SetFrameFillStyle(4000);
ratioPad.SetFrameBorderMode(0);
ratioPad.SetTicks(1,1);
ratioPad.Draw()
ratioPad.cd();
ratioHist=createRatio(dTH1D,gTH1D,outputLog)
ratioHist.GetYaxis().SetRangeUser(0,2)
ratioHist.SetTitle('Ratio;m_{ggg} [GeV];Data/MC')
ratioPad.Draw()
ratioHist.Draw()
gCanvas.BuildLegend()
setStyle(gCanvas)

gCanvas.Print('ratio.pdf')

of.Write()
of.Close()
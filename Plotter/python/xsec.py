import logging

PB = 1.
pb = PB
FB = 1.e-3
fb = FB

xsecs = {
    'DoubleMuon'                                                   : 1.,
    'DoubleEG'                                                     : 1.,
    'MuonEG'                                                       : 1.,
    'SingleMuon'                                                   : 1.,
    'SingleElectron'                                               : 1.,
    'Tau'                                                          : 1.,

    'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'  :  18610.       * PB,
    'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'      :   6025.2      * PB,

    'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'               :    831.76     * PB,
    'TTTo2L2Nu_13TeV-powheg'                                       :     87.31     * PB,
    'TT_TuneCUETP8M1_13TeV-powheg-pythia8'                         :    831.76     * PB,

    'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8'         :      0.2529   * PB,
    'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                  :      0.5297   * PB,
    'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8' :      0.2043   * PB,
    'TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8'  :      0.4062   * PB,

    'tZq_ll_4f_13TeV-amcatnlo-pythia8_TuneCUETP8M1'                :      0.0758   * PB,

    'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'           :  61526.7      * PB,

    'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'              :    117.864    * PB,
    'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'             :    489.       * PB,

    'WWTo2L2Nu_13TeV-powheg'                                       :     10.481    * PB,
    'WWTo4Q_13TeV-powheg'                                          :     45.20     * PB,
    'WWToLNuQQ_13TeV-powheg'                                       :     43.53     * PB,
    'WW_TuneCUETP8M1_13TeV-pythia8'                                :     63.21     * PB,

    'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8'               :     10.71     * PB,
    'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8'                 :      3.05     * PB,
    'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8'                  :      5.60     * PB,
    'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8'                   :      4.42965  * PB,
    'WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'               :      5.29     * PB,
    'WZ_TuneCUETP8M1_13TeV-pythia8'                                :     47.13     * PB,

    'ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8'                    :      6.842    * PB,
    'ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8'                 :      4.04     * PB,
    'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8'                  :      3.28     * PB,
    'ZZTo2L2Nu_13TeV_powheg_pythia8'                               :      0.564    * PB,
    'ZZTo4L_13TeV_powheg_pythia8'                                  :      1.256    * PB * 1.1,
    'ZZTo4L_13TeV-amcatnloFXFX-pythia8'                            :      1.212    * PB * 1.1,
    'ZZ_TuneCUETP8M1_13TeV-pythia8'                                :     16.523    * PB,

    'GluGluToZZTo2e2mu_BackgroundOnly_13TeV_MCFM'                  :      0.003194 * PB * 1.7,
    'GluGluToZZTo2e2tau_BackgroundOnly_13TeV_MCFM'                 :      0.003194 * PB * 1.7,
    'GluGluToZZTo2mu2tau_BackgroundOnly_13TeV_MCFM'                :      0.003194 * PB * 1.7,
    'GluGluToZZTo4e_BackgroundOnly_13TeV_MCFM'                     :      0.001586 * PB * 1.7,
    'GluGluToZZTo4mu_BackgroundOnly_13TeV_MCFM'                    :      0.001586 * PB * 1.7,
    'GluGluToZZTo4tau_BackgroundOnly_13TeV_MCFM'                   :      0.001586 * PB * 1.7,
    'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8'              :      0.003194 * PB * 1.7,
    'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8'             :      0.003194 * PB * 1.7,
    'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8'            :      0.003194 * PB * 1.7,
    'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8'                 :      0.001586 * PB * 1.7,
    'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8'                :      0.001586 * PB * 1.7,
    'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8'               :      0.001586 * PB * 1.7,

    'WWW_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                      :      0.1651   * PB,
    'WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                      :      0.1651   * PB,
    'WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                      :      0.05565  * PB,
    'ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                      :      0.01398  * PB,

    'HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8'                :      1.605    * FB, # LO output from pythia8
}


def getXsec(sample):
    if sample in xsecs:
        return xsecs[sample]
    else:
        logging.error('Failed to find cross section for {0}.'.format(sample))
        return 0.
from root_numpy import root2array, tree2array, fill_hist
import ROOT
import numpy as np
from array import array
from ROOT import TH2D
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



#"/storage1/users/wl33/AMPT/ampttree_PbPb_r0.root"
#read from root file
rfile_ampttree_PbPb_r0 = ROOT.TFile("preSelectedData.root")
#root_file to tree
intree_ampttree_PbPb_r0 = rfile_ampttree_PbPb_r0.Get('ampttree_particles')

#intree_ampttree_PbPb_r0.Print()

#get number of events in the tree
nampttree_PbPb_r0Evns=intree_ampttree_PbPb_r0.GetEntries()



max_nmult = intree_ampttree_PbPb_r0.GetMaximum("nmult")
print 'max :    ', max_nmult
min_nmult = intree_ampttree_PbPb_r0.GetMinimum("nmult")
print 'min :    ', min_nmult 

print 'number of ivents ampttree:  ' , nampttree_PbPb_r0Evns



fill_value=0 
length=5000
#length=4
#nampttree_PbPb_r0Evns=10

b_lt13 = tree2array(intree_ampttree_PbPb_r0,
    branches=[('pt', fill_value, length), ('eta', fill_value, length), ('phi', fill_value, length), ('pid', fill_value, length)],
    selection='b < 13 && nmult<=5000 ',
    start=0, stop=nampttree_PbPb_r0Evns)
    
b_gt13 = tree2array(intree_ampttree_PbPb_r0,
    branches=[('pt', fill_value, length), ('eta', fill_value, length), ('phi', fill_value, length), ('pid', fill_value, length)],
    selection='b > 13 && nmult<=5000',
    start=0, stop=nampttree_PbPb_r0Evns)

#change the shape---------------------------------------------------------
b_lt13=b_lt13.view((b_lt13.dtype[0], len(b_lt13.dtype.names)))
b_gt13=b_gt13.view((b_gt13.dtype[0], len(b_gt13.dtype.names)))
b_lt13=b_lt13.transpose((0,2,1))
b_gt13=b_gt13.transpose((0,2,1))


np.save('b_lt_5k',b_lt13)
np.save('b_gt_5k',b_gt13)



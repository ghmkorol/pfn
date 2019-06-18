from root_numpy import root2array, tree2array, fill_hist
import ROOT
import numpy as np
from array import array
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


#read from root file
rfile_ampttree_PbPb_r0 = ROOT.TFile("/storage1/users/wl33/AMPT/ampttree_PbPb_r0.root")
#root_file to tree
intree_ampttree_PbPb_r0 = rfile_ampttree_PbPb_r0.Get('ampttree_particles')

#Print tree
#intree_ampttree_PbPb_r0.Print()

#get number of events in the tree
nampttree_PbPb_r0Evns=intree_ampttree_PbPb_r0.GetEntries()
max_nmult = intree_ampttree_PbPb_r0.GetMaximum("nmult")
min_nmult = intree_ampttree_PbPb_r0.GetMinimum("nmult")

print 'max :    ', max_nmult
print 'min :    ', min_nmult 
print 'number of ivents ampttree:  ' , nampttree_PbPb_r0Evns



fill_value=np.nan 
length=max_nmult
length=4
nampttree_PbPb_r0Evns=10

	
#array of arrays----------------------------------------------------
b_lt13 = tree2array(intree_ampttree_PbPb_r0,
    branches=[('sqrt(pow(px,2)+pow(py,2))', fill_value, length), ('py/px', fill_value, length), ('sqrt(pow(px,2)+pow(py,2))/pz', fill_value, length)],
    selection='b < 13 && (npart-50)<100',
    start=0, stop=nampttree_PbPb_r0Evns)
    
b_gt13 = tree2array(intree_ampttree_PbPb_r0,
    branches=[('sqrt(pow(px,2)+pow(py,2))', fill_value, length), ('py/px', fill_value, length), ('sqrt(pow(px,2)+pow(py,2))/pz', fill_value, length)],
    selection='b > 13 && (npart-50)<100',
    start=0, stop=nampttree_PbPb_r0Evns)

b = tree2array(intree_ampttree_PbPb_r0,
    branches=['b'],
    start=0, stop=nampttree_PbPb_r0Evns)
    
npart = tree2array(intree_ampttree_PbPb_r0,
    branches=['npart'],
    start=0, stop=nampttree_PbPb_r0Evns)



#to check the initial shape and type of array
print 'b_lt13.shape ', b_lt13.shape
print 'b_lt13.dtype', b_lt13.dtype
print 'type(b_lt13)', type(b_lt13)
print 'b_lt13=', b_lt13

print '********* b_gt13  '

print 'b_gt13.shape ', b_gt13.shape
print 'b_gt13.dtype', b_gt13.dtype
print 'type(b_gt13)', type(b_gt13)
print 'b_gt13=', b_gt13


#change the shape---------------------------------------------------
b_lt13=b_lt13.view((b_lt13.dtype[0], len(b_lt13.dtype.names)))
b_gt13=b_gt13.view((b_gt13.dtype[0], len(b_gt13.dtype.names)))
#transpose-----------------------------------------------------------
b_lt13=b_lt13.transpose((0,2,1))
b_gt13=b_gt13.transpose((0,2,1))


#to check  and type of array after reshape and trasformation
print 'b_lt13.shape ', b_lt13.shape
print 'b_lt13.dtype', b_lt13.dtype
print 'type(b_lt13)', type(b_lt13)
print 'b_lt13=', b_lt13

print '********* b_gt13  '

print 'b_gt13.shape ', b_gt13.shape
print 'b_gt13.dtype', b_gt13.dtype
print 'type(b_gt13)', type(b_gt13)
print 'b_gt13=', b_gt13



print 'b', b
print 'npart', npart

#save to file
np.save('b_lt13',b_lt13)
np.save('b_gt13',b_gt13)
#read from file
#results = np.load('b_lt13.npy')
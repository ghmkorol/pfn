from root_numpy import root2array, tree2array, fill_hist
import ROOT
import numpy as np
from array import array
from ROOT import TH2D
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



#read from root file
rfile_ampttree_PbPb_r0 = ROOT.TFile("/storage1/users/wl33/AMPT/ampttree_PbPb_r0.root")
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



fill_value=np.nan 
length=max_nmult
#length=50
#nampttree_PbPb_r0Evns=100





#simple array---------------------------------------------------------
npart_b_lt13 = tree2array(intree_ampttree_PbPb_r0,
    branches=['npart'],
    selection='b < 13',
    start=0, stop=nampttree_PbPb_r0Evns)
    
npart_b_gt13 = tree2array(intree_ampttree_PbPb_r0,
    branches=['npart'],
    selection='b > 13',
    start=0, stop=nampttree_PbPb_r0Evns)

	
	

	


#array of arrays-----------------------------------------------------
ptBranch='sqrt(pow(px,2)+pow(py,2))'
phiBranch='atan(py/px)+(px<0)*(TMath::Pi()-2*(py<0)*TMath::Pi())'
etaBranch='-log(tan(atan(sqrt(pow(px,2)+pow(py,2))/fabs(pz))/2))*(pz/fabs(pz))'

b_lt13 = tree2array(intree_ampttree_PbPb_r0,
    branches=[(ptBranch, fill_value, length), (phiBranch, fill_value, length), (etaBranch, fill_value, length)],
    selection='b < 13',
    #object_selection={'fabs(-log(tan(atan(sqrt(pow(px,2)+pow(py,2))/pz)/2)))<5': [ptBranch, phiBranch, etaBranch ]},
    start=0, stop=nampttree_PbPb_r0Evns)
    
b_gt13 = tree2array(intree_ampttree_PbPb_r0,
    branches=[(ptBranch, fill_value, length), (phiBranch, fill_value, length), (etaBranch, fill_value, length)],
    selection='b > 13',
    #object_selection={'fabs(-log(tan(atan(sqrt(pow(px,2)+pow(py,2))/pz)/2)))<5': [ptBranch, phiBranch, etaBranch ]},
    start=0, stop=nampttree_PbPb_r0Evns)

#change the shape---------------------------------------------------------
b_lt13=b_lt13.view((b_lt13.dtype[0], len(b_lt13.dtype.names)))
b_gt13=b_gt13.view((b_gt13.dtype[0], len(b_gt13.dtype.names)))
b_lt13=b_lt13.transpose((0,2,1))
b_gt13=b_gt13.transpose((0,2,1))



#---fi------replace 'py/px' with its arctan
#b_lt13[:,:,1]=np.arctan(b_lt13[:,:,1])
#---thau------replace 'sqrt(pow(px,2)+pow(py,2))/pz' with its arctan
#b_lt13[:,:,2]=np.arctan(b_lt13[:,:,2])
#---n------replace thau with -ln(tan(thau/2))
#b_lt13[:,:,2]=-np.log(np.tan(b_lt13[:,:,2]/2))


#---fi------replace 'py/px' with its arctan
#b_gt13[:,:,1]=np.arctan(b_gt13[:,:,1])
#---thau------replace 'sqrt(pow(px,2)+pow(py,2))/pz' with its arctan
#b_gt13[:,:,2]=np.arctan(b_gt13[:,:,2])
#---n------replace thau with -ln(tan(thau/2))
#b_gt13[:,:,2]=-np.log(np.tan(b_gt13[:,:,2]/2))




'''####     PRINT     #############

#print arrays info

print 'b_lt13.shape ', b_lt13.shape
print 'b_lt13.dtype', b_lt13.dtype
print 'type(b_lt13)', type(b_lt13)
print 'b_lt13=', b_lt13

print '********* b_gt13  '

print 'b_gt13.shape ', b_gt13.shape
print 'b_gt13.dtype', b_gt13.dtype
print 'type(b_gt13)', type(b_gt13)
print 'b_gt13=', b_gt13

print###################################
'''
print 'b_lt13.shape ', b_lt13.shape
print 'b_lt13.dtype', b_lt13.dtype
print 'type(b_lt13)', type(b_lt13)
print 'b_lt13='
print b_lt13

print '********* b_gt13  '

print 'b_gt13.shape ', b_gt13.shape
print 'b_gt13.dtype', b_gt13.dtype
print 'type(b_gt13)', type(b_gt13)
print 'b_gt13='
print  b_gt13
# condition by |n|<5
b_lt13=b_lt13[np.fabs(b_lt13[:,:,2])<5]
b_gt13=b_gt13[np.fabs(b_gt13[:,:,2])<5]




print 'b_lt13.shape ', b_lt13.shape
print 'b_lt13.dtype', b_lt13.dtype
print 'type(b_lt13)', type(b_lt13)
print 'b_lt13='
print b_lt13

print '********* b_gt13  '

print 'b_gt13.shape ', b_gt13.shape
print 'b_gt13.dtype', b_gt13.dtype
print 'type(b_gt13)', type(b_gt13)
print 'b_gt13='
print b_gt13





mask_lt = np.all(np.isnan(b_lt13) | np.equal(b_lt13, 0), axis=1)
b_lt13=b_lt13[~mask_lt]

mask_gt = np.all(np.isnan(b_gt13) | np.equal(b_gt13, 0), axis=1)
b_gt13=b_gt13[~mask_gt]




print 'b_lt13.shape ', b_lt13.shape
print 'b_lt13.dtype', b_lt13.dtype
print 'type(b_lt13)', type(b_lt13)
print 'b_lt13='
print b_lt13

print '********* b_gt13  '

print 'b_gt13.shape ', b_gt13.shape
print 'b_gt13.dtype', b_gt13.dtype
print 'type(b_gt13)', type(b_gt13)
print 'b_gt13='
print b_gt13




#############################################
#______________histogram of Pt
#############################################
fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)
#extract [:,branch] for all events
# plt_b_lt13 = b_lt13[:,:,0].ravel()   /sends to d1
plt_b_lt13 = b_lt13[:,0]
plt_b_gt13 = b_gt13[:,0]


bins = np.linspace(0, 2, 100)

ax1.hist(plt_b_lt13, bins, alpha=0.5,
                                    density=True,
                                    label='b<13',
                                    histtype='stepfilled', 
                                     ec="k")
                                    
ax1.hist(plt_b_gt13, bins, alpha=0.5, 
                                    density=True,
                                    label='b>13', 
                                    histtype='stepfilled', 
                                    ec="k")
ax1.set_xlabel('Pt')
ax1.set_ylabel('density')
ax1.set_title('Histogram of Pt \n cut: |$\eta$|<5')
ax1.legend(loc='upper right')
fig1.savefig("pt.png")

#############################################
#_____end________histogram of Pt
#############################################



#############################################
#______________histogram of phi
#############################################

fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1)
#extract [:,branch] for all events
plt_b_lt13 = b_lt13[:,1]
plt_b_gt13 = b_gt13[:,1]

bins = np.linspace(-4, 4, 100)
#bins = 100
ax2.hist(plt_b_lt13, bins, alpha=0.5,
                                    density=True,
                                    label='b<13',
                                    histtype='stepfilled', 
                                     ec="k")
                                    
ax2.hist(plt_b_gt13, bins, alpha=0.5, 
                                    density=True, 
                                    label='b>13', 
                                    histtype='stepfilled', 
                                    ec="k")
ax2.set_xlabel('$\phi$')
ax2.set_ylabel('density')
ax2.set_title('Histogram of $\phi$ \n cut: |$\eta$|<5')
ax2.legend(loc='upper right')
fig2.savefig("phi.png")

#############################################
#_____end________histogram of phi
#############################################


#############################################
#______________histogram of etta
#############################################

fig3 = plt.figure()
ax3 = fig3.add_subplot(1, 1, 1)
#extract [:,branch,:] for all events
plt_b_lt13 = b_lt13[:,2]
plt_b_gt13 = b_gt13[:,2]
#plt_b_lt13 = b_lt13[:,:,2].ravel() 
#plt_b_gt13 = b_gt13[:,:,2].ravel() 

bins = np.linspace(-6, 6, 100)
#bins = 100
ax3.hist(plt_b_lt13, bins, alpha=0.5,
                                    density=True,
                                    label='b<13',
                                    histtype='stepfilled', 
                                     ec="k")
                                    
ax3.hist(plt_b_gt13, bins, alpha=0.5, 
                                    density=True, 
                                    label='b>13', 
                                    histtype='stepfilled', 
                                    ec="k")
ax3.set_xlabel('$\eta$')
ax3.set_ylabel('density')
ax3.set_title('Histogram of $\eta$ \n cut: |$\eta$|<5')
ax3.legend(loc='upper right')
fig3.savefig("eta.png")

#############################################
#_____end________histogram of etta
#############################################


exit()




#############################################
#______________histogram of number of parcles
#############################################

#convert to 1d array
npart_b_lt13=npart_b_lt13.view(npart_b_lt13.dtype[0])
npart_b_gt13=npart_b_gt13.view(npart_b_gt13.dtype[0])

bins = np.linspace(0, 300, 100)
plt.hist(npart_b_lt13, bins, alpha=0.5,
                                    density=True, 
                                    label='b<12',
                                    histtype='stepfilled', 
                                    ec="k")
                                    
plt.hist(npart_b_gt13, bins, alpha=0.5, 
                                    density=True, 
                                    label='b>12', 
                                    histtype='stepfilled', 
                                    ec="k")
plt.xlabel('npart')
plt.ylabel('Probability')
plt.title('Histogram of number of parcles')
plt.legend(loc='upper right')

plt.show()
#############################################
#_____end________histogram of number of parcles
#############################################


# and convert the TTree into an array
array_sampttree_PbPb_r0 = tree2array(intree_ampttree_PbPb_r0,
    branches=[('px+0',fill_value,length), ('py+0',fill_value,length), ('pz+0',fill_value,length)],
    start=0, stop=nampttree_PbPb_r0Evns)


#to check the initial shape and type of array
print 'array_sampttree_PbPb_r0.shape ', array_sampttree_PbPb_r0.shape
print 'array_sampttree_PbPb_r0.dtype', array_sampttree_PbPb_r0.dtype
print 'type(array_sampttree_PbPb_r0)', type(array_sampttree_PbPb_r0)
print 'array_sampttree_PbPb_r0=', array_sampttree_PbPb_r0

print '---------------------------------------'
print '---------------------------------------'
print '---------------------------------------'
array_sampttree_PbPb_r0 = array_sampttree_PbPb_r0.view((array_sampttree_PbPb_r0.dtype[0], len(array_sampttree_PbPb_r0.dtype.names)))
array_sampttree_PbPb_r0=array_sampttree_PbPb_r0.transpose((0,2,1))
print 'array_sampttree_PbPb_r0=', array_sampttree_PbPb_r0, 'shape: ', array_sampttree_PbPb_r0.shape, 'type:', array_sampttree_PbPb_r0.dtype



#extract [:,branch,:] for all event and send to 1d array
plt_b_lt13 = b_lt13[:,:,2].ravel() 
plt_b_gt13 = b_gt13[:,:,2].ravel()
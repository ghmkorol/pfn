# standard library imports
from __future__ import absolute_import, division, print_function

# standard numerical library imports
import numpy as np

# energyflow imports
import energyflow as ef
from energyflow.archs import PFN
from energyflow.datasets import qg_jets
from energyflow.utils import data_split, remap_pids, to_categorical

from numpy.random import RandomState
RNG = RandomState(40)

# attempt to import sklearn
try:
    from sklearn.metrics import roc_auc_score, roc_curve
except:
    print('please install scikit-learn in order to make ROC curves')
    roc_curve = False

# attempt to import matplotlib
try:
    import matplotlib.pyplot as plt
except:
    print('please install matploltib in order to make plots')
    plt = False

################################### SETTINGS #############
# the commented values correspond to those in 1810.05165
##########################################################

# data controls, can go up to 2000000 for full dataset
train, val, test = 75000, 10000, 15000
# train, val, test = 1000000, 200000, 200000
use_pids = False

# network architecture parameters
Phi_sizes, F_sizes = (10, 10, 16), (10, 10, 10)
# Phi_sizes, F_sizes = (100, 100, 256), (100, 100, 100)

# network training parameters
num_epoch = 5
batch_size = 500

#########################################################

# load data

b_lt13 = np.load('b_lt_5k.npy')
b_gt13 = np.load('b_gt_5k.npy')


X = np.concatenate([b_lt13, b_gt13])
y = np.ones(X.shape[0]) # 1: b_gt13; 0: b_lt13
y[b_lt13.shape[0]:] *= 0

train, val, test = int(y.shape[0]*.75), int(y.shape[0]*.1), int(y.shape[0]*.15)



permute = RNG.permutation(y.shape[0])
X = X[permute]
X=np.nan_to_num(X)

y = y[permute]
Y = to_categorical(y, num_classes=2)

'''
for x in X:
    mask = x[:,0] > 0
    yphi_avg = np.average(x[mask,1:3], weights=x[mask,0], axis=0)
    x[mask,1:3] -= yphi_avg
    x[mask,0] /= x[:,0].sum()/10'''


# handle particle id channel
if use_pids:
    remap_pids(X, pid_i=3)
else:
    X = X[:,:,:3]

print('Finished preprocessing')

# do train/val/test split 
(X_train, X_val, X_test,
 Y_train, Y_val, Y_test) = data_split(X, Y, val=val, test=test)

print('Done train/val/test split')
print('Model summary:')

# build architecture
pfn = PFN(input_dim=X.shape[-1], Phi_sizes=Phi_sizes, F_sizes=F_sizes)

# train model
pfn.fit(X_train, Y_train,
          epochs=num_epoch,
          batch_size=batch_size,
          validation_data=(X_val, Y_val),
          verbose=1)

# get predictions on test data
preds = pfn.predict(X_test, batch_size=1000)


# get ROC curve if we have sklearn
if roc_curve:
    pfn_fp, pfn_tp, threshs = roc_curve(Y_test[:,1], preds[:,1])

    # get area under the ROC curve
    auc = roc_auc_score(Y_test[:,1], preds[:,1])
    print()
    print('PFN AUC:', auc)
    print()

    # make ROC curve plot if we have matplotlib
    if plt:

     # get multiplicity and mass for comparison
        masses = np.asarray([ef.ms_from_p4s(ef.p4s_from_ptyphims(x).sum(axis=0)) for x in X])
        mults = np.asarray([np.count_nonzero(x[:,0]) for x in X])
       # mass_fp, mass_tp, threshs = roc_curve(Y[:,1], -masses)
        #mult_fp, mult_tp, threshs = roc_curve(Y[:,1], -mults)

        # some nicer plot settings 
        plt.rcParams['figure.figsize'] = (4,4)
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['figure.autolayout'] = True

        # plot the ROC curves
        plt.plot(pfn_tp, 1-pfn_fp, '-', color='black', label='PFN')
       # plt.plot(mass_tp, 1-mass_fp, '-', color='blue', label='Jet Mass')
       # plt.plot(mult_tp, 1-mult_fp, '-', color='red', label='Multiplicity')

        # axes labels
        plt.xlabel('b<13')
        plt.ylabel('b>13')

        # axes limits
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.text(0.6, 0.8, r'pfn auc='+str(round(auc,2)), fontsize=10)
        # make legend and show plot
        plt.legend(loc='lower left', frameon=False)
        plt.savefig("plot_run1_5k.png")
        plt.show()
        
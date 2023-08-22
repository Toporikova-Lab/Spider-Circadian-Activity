from operator import ne
from modules.utils.trainLoader import loadData
import numpy as np
from modules.utils.backprop import Perceptron, progressBar
import os

# load input patterns for the training data
# using the files stored in trainData
# crunching the time intervals down to hours
T, I = loadData(60, 'trainData') 

# convert targets into dead|not-dead
T = np.where(T == 215, 1, 0)

print('Inputs:', len(I[0]), 'Outputs:', 2)

#make perceptron with 3 hidden layers, 216 input units, 18 output units 
p = Perceptron(h=5, i=216, o=1)

# use the built in training function to train
# I built it
p.train(I, T, neps=20000, eta=0.005, mew=0.05)

# save the results
savedir = 'modules{0}saves{0}'.format(os.sep)
p.save(ih = savedir+'ihShallow1.npy', ho = savedir+'hoShallow1.npy')
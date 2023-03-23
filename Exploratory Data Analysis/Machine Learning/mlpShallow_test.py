from modules.utils.backprop import Perceptron, section
from modules.utils.trainLoader import loadData
import os
import numpy as np
import pandas as pd

# load testing data
T, I = loadData(60, 'testData')

# 1 means alive, 0 means dead
T1 = np.where(T == 215, 1, 0)

#dummy class, for data to be loaded into
p = Perceptron(h = 0, i = 0, o = 0)

#load in the already trained data
savedir = 'modules{0}saves{0}'.format(os.sep)
p.load(ih = savedir+'ihShallow.npy', ho = savedir+'hoShallow.npy')

# using the test set, see how far we are from what we want
fpos, fneg = 0, 0
pos, neg = 0, 0
ncorrect = 0
outs = []
for i in range(len(I)):
    
    # get the output
    o = list(p.test(I[i]))[0]
    
    """
    line-by-line data collection
    """
    # target vs. actual
    outs.append([T[i], o])
    
    threshold = .15
    if T1[i] == 1: #spider alive
        neg += 1
        if o > threshold:
            ncorrect += 1
        else:
            fpos += 1
    elif T1[i] == 0:
        pos += 1
        if o <= threshold:
            ncorrect += 1
        else:
            fneg += 1
df = pd.DataFrame(data=outs, columns=['Time of death', 'MLP Output'])
print('\n',section('Shallow Perceptron'))
print('Threshold: outputs >', threshold, 'are considered "alive"')
print('False Positives:', str(fpos)+'/'+str(neg), 'False Negatives:', str(fneg)+'/'+str(pos))
print('Total Accuracy:', str(100*ncorrect/len(T1)) + '%')
print(df)
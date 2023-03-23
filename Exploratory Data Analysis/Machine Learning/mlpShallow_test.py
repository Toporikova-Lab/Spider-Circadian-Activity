from modules.utils.backprop import Perceptron
from modules.utils.trainLoader import loadData
import os
import numpy as np

# load testing data
T, I = loadData(60, 'testData')

# 1 means alive, 0 means dead
T = np.where(T == 215, 1, 0)

#dummy class, for data to be loaded into
p = Perceptron(h = 0, i = 0, o = 0)

#load in the already trained data
savedir = 'modules{0}saves{0}'.format(os.sep)
p.load(ih = savedir+'ihShallow.npy', ho = savedir+'hoShallow.npy')

# using the test set, see how far we are from what we want
fpos, fneg = 0, 0
pos, neg = 0, 0
ncorrect = 0
for i in range(len(I)):
    
    # get the output
    o = list(p.test(I[i]))[0]
    
    """
    line-by-line printouts. ignore.
    """
    # ot = 'Yes' if o[0] > .5 else 'No'
    # t = 'Yes' if T[i] == 1 else 'No'
    # print target vs. actual
    # print('Spider #' + str(i+1), 'Did it survive? '+ t + '. Do we think it survived? ' + ot, 'Literal output', o)
    
    threshold = .5
    if T[i] == 1: #spider alive
        neg += 1
        if o > threshold:
            ncorrect += 1
        else:
            fpos += 1
    elif T[i] == 0:
        pos += 1
        if o <= threshold:
            ncorrect += 1
        else:
            fneg += 1

print('False Positives:', str(fpos)+'/'+str(neg), 'False Negatives:', str(fneg)+'/'+str(pos))
print('Total Accuracy:', str(100*ncorrect/len(T)) + '%')
"""HW02 Part 2"""

import numpy as np
import os
from ..utils.backprop import Perceptron, section
#===========================================================Part 2==========================================================
def readData(fileName):    
    f = open(fileName, 'r').read().split(' ')
    data = []
    target = []
    i = 0
    while i < len(f)-14*14:
        data.append([int(n[-1]) for n in f[i:14*14+i]])
        i += 14*14
        target.append([int(n[-1]) for n in f[i:i+10]])
        i+=10
    return np.array(data), np.array(target)

def visualize(outp, num, d=None):
    if d is None:
        d=readData('digits_train.txt')[0]
    if 'out' not in os.listdir():
        os.mkdir('out')
    f = open('out' + os.sep + outp, 'w')
    i = num*250
    while i < num*250 + 250:
        j = 0             
        while j < 14*14:
                f.write(str(d[i][j:j+14])+'\n')
                j+=14
        i+=1
        
def testClassifier(pt:Perceptron, I, T):
    fpos, fneg = 0,0
    s = ''
    for i in range(len(I)):
        want2 = T[i] == 1
        got2 = pt.test(I[i]) > .2
        if got2 and not want2:
            fpos+=1
        elif not got2 and want2:
            fneg+=1
    return fpos, fneg
    
def main():
    print(section('Part 2'))
    pt=Perceptron(5, 196, 1)
    
    #try loading data
    try:
        pt.load()
    except:
        #read from the files
        inTrain, tarTrain = readData('..{0}HW02{0}digits_train.txt'.format(os.sep))
        
        #train the perceptron
        print('Training 2|Not-2')
        tarTrain = tarTrain[:,2]
        print('Training for 2|not-2')
        pt.train(inTrain, tarTrain, neps=1000, eta=.5)
        
        #save the data
        pt.save()
    
    #test the perceptron
    print('Results for 2|Not-2')
    inTest, tarTest = readData('..{0}HW02{0}digits_test.txt'.format(os.sep))
    tarTest = tarTest[:,2]
    fpos, fneg = testClassifier(pt, inTest, tarTest)
    print('False Positives: ({0} / 2250)\nFalse Negatives: ({1} / 250)'.format(fpos, fneg))
    
if __name__ == '__main__':
    main()

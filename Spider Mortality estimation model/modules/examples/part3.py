"""HW03 Part 3"""
from re import M
from ..utils.backprop import Perceptron, printTable, section
import numpy as np
from part2 import readData, testClassifier
import os, sys
from argparse import ArgumentParser as argp

par = argp()
par.add_argument('--ext', default='', type=str, dest='ext')
par.add_argument('--neps', default=1000, type=int, dest='neps')
par.add_argument('--eta', default=.5, type=float, dest='eta')
par.add_argument('--mew', default=0, type=float, dest='mew')
args = dict(par.parse_args()._get_kwargs())

def testClassifier(pt:Perceptron, I):
    matrix = []
    j = -1
    for i in range(len(I)):
        if i % 250 == 0:
            j += 1
            matrix.append([0]*10)
        o = pt.test(I[i])
        for digit in range(10):
            if o[digit] > .2:
                matrix[j][digit] += 1
    return matrix

def main():
    print(section('Part 3'))
    pt=Perceptron(5, 196, 10)
    ih, ho = 'fullMontyIH', 'fullMontyHO'
    msgF = 'hypers' 
    
    #get arguments
    ext = args['ext']
    neps = args['neps']
    eta = args['eta']
    mew = args['mew']
    
    for name in (ih, ho, msgF):
        name += str(ext) + '.npy'
    
    # if len(sys.argv) > 1:
    ih += ext + '.npy'
    ho += ext + '.npy'
    msgF += ext + '.npy'
    
    #try loading data
    try:
        pt.load(ih, ho)
        msg = np.load(msgF)
    except:
        #read from the files
        inTrain, tarTrain = readData('..{0}HW02{0}digits_train.txt'.format(os.sep))
        #train the perceptron
        tarTrain = tarTrain
        print('Training Full-Digit Classifier')
        pt.train(inTrain, tarTrain, neps=neps, eta=eta, mew=mew)
        #save the data
        pt.save(ih, ho)
        msg='Training Episodes: '+ str(neps) + ' Weight Decay: ' + str(eta)
        np.save(msgF, msg)
    
    #test the perceptron
    inTest, tarTest= readData('..{0}HW02{0}digits_test.txt'.format(os.sep))
    matrix = testClassifier(pt, inTest)

    #informative printout
    print(msg)
    header = '  '
    for num in range(10):
        header += '|{0:^10}'.format(num)
    print(header + '|\n  ' + '='*111)
    printTable(matrix, leftHeaders=True)
    
if __name__ == '__main__':
    main()

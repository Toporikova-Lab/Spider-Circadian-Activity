"""HW03 Part 4"""
from ..utils.backprop import Perceptron, printTable, section
import numpy as np
from part2 import readData, testClassifier
import os
import matplotlib.pyplot as plt


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

def getMatrix(ih, ho):
    pt=Perceptron(5, 196, 10)
    pt.load(ih, ho)
    inTest, _= readData('..{0}HW02{0}digits_test.txt'.format(os.sep))
    return testClassifier(pt, inTest)

def printMatrix(matrix, msg):
    print(msg)
    header = '  '
    for num in range(10):
        header += '|{0:^10}'.format(num)
    print(header + '|\n  ' + '='*111)
    printTable(matrix, leftHeaders=True)
    print()

def confPlot(matrix,  title): #credit: https://stackoverflow.com/questions/37711538/matplotlib-3d-axes-ticks-labels-and-latex
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    matrix = np.array(matrix)

    xpos = [range(matrix.shape[0])]
    ypos = [range(matrix.shape[1])]
    xpos, ypos = np.meshgrid(xpos, ypos)
    xpos = xpos.flatten('F')
    ypos = ypos.flatten('F')
    zpos = np.zeros_like(xpos)

    dx = 0.5 * np.ones_like(zpos)
    dy = dx.copy()
    dz = matrix.flatten()

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz/250, color='b', zsort='average')
    
    plt.xlabel('Expected')
    plt.ylabel('Result')
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel('Confidence Result = Expected')
    plt.title(title)
    ax.set_xticks([i for i in range(10)])
    ax.set_yticks([i for i in range(10)])
    
    plt.show()
    plt.close()

def main():
    print(section('Part 4'))

    #get saved data no momentum
    msg1 = np.load('hypers.npy')
    ih1, ho1 = 'fullMontyIH.npy', 'fullMontyHO.npy'
    
    #saved data for momentum
    msg2 = np.load('hypers0.npy')
    ih2, ho2 = 'fullMontyIH0.npy', 'fullMontyHO0.npy'
    
    #get matrix for no mementum
    mat1 = getMatrix(ih1, ho1)
    
    #get matrix with momentum
    mat2 = getMatrix(ih2, ho2)
    
    #informative printouts
    print(section('No Momentum'))
    printMatrix(mat1, msg1)
    print(section('With Momentum'))
    printMatrix(mat2, msg2)
    
    #plot on 3d histogram
    confPlot(mat1, 'No Momentum')
    confPlot(mat2, 'With Momentum')
   
    try:
        import webbrowser as wb
        wb.open('https://github.com/simondlevy/boscoj24/blob/main/csci315/HW03/report.md')
    except:
        print('If you are reading this, I gave up on the dependency auto-installer')
        print('Just read the report.md file from Github in your webbrowser')
    
if __name__ == '__main__':
    main()

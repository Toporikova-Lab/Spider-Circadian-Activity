import numpy as np
from ..utils.backprop import Perceptron
#===========================================================Part 1==========================================================
def section(name):
    return '\n{0:=^100s}'.format(name)

pt = Perceptron(5, 2, 1)
binaryInputs = np.array([
                    [0,0],
                    [0,1],
                    [1,0],
                    [1,1]
])
xorOutputs = np.array([
                        [0],
                        [1],
                        [1],
                        [0]
])
print(section('Part 1'))
print('Training XOR:')
pt.train(binaryInputs, xorOutputs, neps=10000, eta=0.5)
print()

for i in binaryInputs:
    print(i, '->', pt.test(i))

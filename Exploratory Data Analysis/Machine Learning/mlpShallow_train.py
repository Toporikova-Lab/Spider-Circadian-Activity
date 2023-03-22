from modules.utils.trainLoader import loadData
import numpy as np

# load up target and input patterns for the training data
# we are using the files stored in trainData and crunching the time intervals down to hours
T, I = loadData(60, 'trainData')
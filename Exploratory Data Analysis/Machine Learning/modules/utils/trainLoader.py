"""
Jack Bosco
Functions for loading and saving testing data
"""
from fileinput import filename
import pandas as pd
import numpy as np
import os
from IPython.display import display

def grabDataFiles(dir='trainData'):
    """
    gets a list of numpy matrices from the .csv files in the spider datapack
    """
    data_path = os.path.abspath(os.curdir) + '{0}{1}{0}'.format(os.sep, dir)
    print('Path:', data_path)
    os.chdir(data_path)
    
    dataPack = []
    for filename in os.listdir():
        df = pd.read_csv(filename, header=0, index_col=0)
        df.reset_index(drop=True, inplace=True)
        df.drop(labels='Light', axis=1, inplace=True)
        df.columns = [i for i in range(df.shape[1])]
        #print(df.shape)
        #print(df)
        dataPack.append(np.array(df))
    
    return dataPack

def getDeathTimes(data : np.ndarray):
    """
    Gets the time where the spider has died
    """
    inputPatterns = data.T
    targets = []
    for pattern in inputPatterns:
        np.nan_to_num(pattern, copy=False, nan=-1)
        nanIndices = np.where(pattern == -1)
        if nanIndices[0].size == 0:
            targets.append(len(pattern) - 1)
        else:
            targets.append(nanIndices[0][0])
    #print('target values:', targets)
    return np.array(targets)

def padWithZero(data : np.ndarray):
    """
    Replaces the nan in the numpy array with zeros
    """
    patterns = data.T
    newPs = []
    for pattern in patterns:
        np.nan_to_num(pattern, copy=False, nan=-1)
        padded = np.where(pattern==-1, 0, pattern)
        newPs.append(padded)
    return np.array(newPs)
    
def crunchData(tar, pat, interval):
    """
    Crunches target and pattern arrays down by the interval amount
    60   -> minutes to hours
    1440 -> minutes to days
    """
    subLength = pat.shape[1] // interval
    
    newTar, newPat = [], []
    for j in range(len(tar)):
        t, p = tar[j], pat[j]
        splitT = t // interval
        
        splitP = np.array_split(p, subLength)
        splitP = np.sum(splitP, axis=1)
        
        newTar.append(splitT)
        newPat.append(splitP)
        #print(splitT, splitP)
    return np.array(newTar), np.array(newPat)
    
def main():
    # get the list of data 
    dataPack = grabDataFiles('trainData')
    
    # for each data matrix
    dataChunks = []
    for datafile in dataPack:
        
        # get the list of target outputs
        deathTimes = getDeathTimes(datafile)
        
        # pad the each column with zeros down to the max depth
        newP = padWithZero(datafile)
    
        # use summation to crunch the minute-length intervals to hours (60) or days (1440)
        tCrunch, pCrunch = crunchData(deathTimes, newP, interval=60)
        
        # squash the activity values to 0 or not-0
        sqsh = np.where(pCrunch > 0, 1, 0)
        
        tp = list(zip(tCrunch, sqsh))
        dataChunks.append(tp)
                
    # concatenate data (only applicable when there are multiple files in the directory)
    if len(dataChunks) > 1:
        data = []
        for chunk in dataChunks:
            for pattern in chunk:
                data.append(pattern)
        data = np.array(data)
    else:
        data = np.array(dataChunks[0])
    print(data.shape)
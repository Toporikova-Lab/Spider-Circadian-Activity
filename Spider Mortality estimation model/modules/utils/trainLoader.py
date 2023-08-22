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
    
    dataPack = []
    for filename in os.listdir(data_path):
        df = pd.read_csv(data_path+os.sep+filename, header=0, index_col=0)
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
    
def loadData(timeInterval, dataPack='trainData'):
    # get the list of data 
    dataPack = grabDataFiles(dataPack)
    
    # for each data matrix
    ts, ps = [], []
    for datafile in dataPack:
        
        # get the list of target outputs
        deathTimes = getDeathTimes(datafile)
        
        # pad the each column with zeros down to the max depth
        newP = padWithZero(datafile)
    
        # use summation to crunch the minute-length intervals to hours (60) or days (1440)
        tCrunch, pCrunch = crunchData(deathTimes, newP, interval=timeInterval)
        
        # squash the activity values to 0 or not-0
        sqsh = np.where(pCrunch > 0, 1, 0)
        
        ts.append(tCrunch)
        ps.append(sqsh)
                
    # concatenate data (only applicable when there are multiple files in the directory)
    if len(ts) > 1:
        t, p = [], []
        for i in range(len(ts)):
            for j in range(len(ts[i])):
                t.append(ts[i][j])
                p.append(ps[i][j])
        return np.array(t), np.array(p)
    else:
        return np.array(ts[0]), np.array(ps[0])
import numpy as np
import pandas as pd

"""Rescoring functions used for mitigating misscored actual wake as sleep, and vice versa."""


def consecutive_reverse(data, n, stepsize=1):
    """Returns a list of lists of consecutive integers."""
    lst_ = []
    lst = np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
    for i in lst:
        if len(i) >= n:
            lst_.append(i)
        else:
            pass
    return lst_

def rescore1(data_, epoch='S'):
    """After at least 4 minutes scored as wake, the next 1 minute scored as sleep is rescored wake."""
    data = data_.copy()
    zero_lst = np.flatnonzero(np.array(data)==0)
    if epoch is 'S':
        n = 8
    else:
        n = 4
    if zero_lst.size:
        if zero_lst[0] >= 5:
            data.loc[zero_lst[0]] = 1
        for i in range(len(zero_lst)-1):
            if (zero_lst[i+1] - zero_lst[i]) >= n:
                pd.Series(data).loc[zero_lst[i+1]] = 1
            else:
                pass
    return data


def rescore2(data_):
    """After at least 10 minutes scored as wake, the next 3 minutes scored as sleep are recorded wake."""
    data = data_.copy()
    zero_lst = np.flatnonzero(np.array(data)==0)
    for i in range(len(zero_lst)-1):
        if (zero_lst[i+1] - zero_lst[i]) >= 10 and (zero_lst[i+3] - zero_lst[i+1]) == 2 :
            for j in range(1, 4):
                data.loc[zero_lst[i+j]] = 1
        else:
            pass
    return data


def rescore3(data_):
    """After at least 15 minutes scored as wake, the next 4 minutes scored as sleep are rescored wake."""
    data = data_.copy()
    zero_lst = np.flatnonzero(np.array(data)==0)
    for i in range(len(zero_lst)-1):
        if (zero_lst[i+1] - zero_lst[i]) >= 15 and (zero_lst[i+4] - zero_lst[i+1]) == 3 :
            for j in range(1, 5):
                data.loc[zero_lst[i+j]] = 1
        else:
            pass
    return data


def rescore4(data_):
    """6 minutes or less scored as sleep surrounded by at least 10 minutes (before and after) 
        scored as wake are rescored wake"""
    data = data_.copy()
    zero_lst =np.flatnonzero(np.array(data)==1)
    for i in range(len(zero_lst)-1):
        if (zero_lst[i+1] - zero_lst[i]) >= 2: 
            consec1 = consecutive_reverse(zero_lst[:zero_lst[i]], 10)
            consec2 = consecutive_reverse(zero_lst[zero_lst[i+1]:], 10)
            if (len(consec1), len(consec2)) > (0, 0):
                for j in range(zero_lst[i]+1, zero_lst[i+1]):
                    data.loc[j] = 1
                else:
                    pass
            pass
    return data


def rescore5(data_):
    """10 minutes or less scored as sleep surrounded by at least 20 minutes (before and after) 
        scored as wake are rescored wake"""
    data = data_.copy()
    zero_lst = np.flatnonzero(np.array(data)==0)
    for i in range(len(zero_lst)-1):
        if (zero_lst[i+1] - zero_lst[i]) >= 20:
            consec = consecutive(zero_lst[i+1:], 10)[0]
            conseclen = len(consec)
            lst_consec = consec[-1]
            if zero_lst[i+conseclen+1] - zero_lst[i+conseclen] >= 20:
                for j in range(1, conseclen+1):
                    data.loc[zero_lst[i+j]] = 1
            else:
                pass
        pass
    return data


def rescore(data_):
    """Rescoring using all 5 Webster et al.'s rules."""
    data = data_.copy()
    return rescore5(rescore4(rescore3(rescore2(rescore1(data)))))

def rescored_wake(data_, epoch='S'):
    """Rescores sleep values to wake if there exist at least 15 minutes of wake values before and after the sleep values
    
    Parameter
    ----------
    data_ : array_like
    
    Return
    ----------
    data : array_like
        rescored sleep values to wake 
    """
    data = data_.copy()
    # lst_ = []
    ones_lst = np.flatnonzero(np.array(data)==1)
    if epoch is 'S':
        n = 30
    else:
        n = 15
    for i in range(len(ones_lst)-1):
        if (ones_lst[i+1] - ones_lst[i]) <= n:
            consec1 = consecutive_reverse(ones_lst[:i], 10)
            consec2 = consecutive_reverse(ones_lst[i+1:], 10)
            if len(consec1) > 0 and len(consec2) > 0:
                for j in range(ones_lst[i]+1, ones_lst[i+1]):
                    data.loc[j] = 1
    return data


def rescored_wake2(data_, epoch='S'):
    """Rescore wake values of the last 30 minutes of the data.
    
    Parameter
    ----------
    data_ : array_like
    
    Return
    ----------
    data : array_like
        rescored sleep values to wake if there exist at least 15 minutes of wake values
    """
    data = data_.copy()
    dat1_ = data[-15:-4].copy()
    ones_lst = np.flatnonzero(np.array(dat1_)==1)
    if epoch is 'S':
        n = 14
    else:
        n = 7
    if ones_lst.size:
        for i in range(len(ones_lst)-1):
            if (ones_lst[i+1] - ones_lst[i]) >= n:
                for j in range(ones_lst[i]+1, ones_lst[i+1]):
                    data.loc[dat1_.index[j]] = 1
    return data

def rescored_sleep(data_, epoch='S'):
    """After at least 15 minutes scored as wake, the next 1 minute scored as sleep is rescored wake.
    
    Parameter
    ----------
    data_ : array_like
    
    Return
    ----------
    data : array_like
        rescored wake values to sleep if there exist at least 15 minutes of sleep values
    """
    data = data_.copy()
    ones_lst = np.flatnonzero(np.array(data)==1)
    if epoch is 'S':
        n = 30
    else:
        n = 15
    if ones_lst.size:
        for i in range(len(ones_lst)-1):
            if (ones_lst[i+1] - ones_lst[i]) >= n: # and (ones_lst[i+2] - ones_lst[i+1]) > 1 :
                data.loc[ones_lst[i+1]] = 0
    return data


def rescored_sleep5(data_, epoch='S'):
    """After at least 15 minutes scored as sleep, the last 5 minutes of wake will be rescored as sleep.
    
    Parameter
    ----------
    data_ : array_like
    
    Return
    ----------
    data : array_like
        rescored the last 5 minutes of wake values to sleep
    """
    data = data_.copy()
    dat1_ = data_[-20:].copy()
    ones_lst = np.flatnonzero(np.array(dat1_)==1)
    if epoch is 'S':
        n = 30
        m = 10
    else:
        n = 15
        m = 5
    if ones_lst.size:
        if ones_lst[0] == n:
            for i in dat1_[-m:].index:
                data.loc[i] = 0
        else:
            pass
    return data

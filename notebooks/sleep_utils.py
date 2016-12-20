from __future__ import division
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as ss
import seaborn as sns
from scipy.ndimage import convolve1d
import itertools
from peakdetect import peakdetect


def getwindow(signal, window_duration = 16, window_interval=1, f_s = 4):
    """
    Function that divides a signal into windows
    
    INPUT
        signal:          1d array containing the signal
        time_signal:     1d array containing the time of the signal
        window_duration: duration of one window in seconds
        window_interval: interval at which the window will slide (default value: 1sec)
                         signal must contain values divisible by the window_interval
        f_s:             sampling frequency; unit is in Hz (default value: 300Hz)
                         
    OUTPUT
        signal_segments: list containing array of values per window
        time_segments:   list containing array of time per window
                         
    """
    time_signal = np.arange(len(signal))*1/f_s
    start_index = np.arange(len(signal))[(time_signal%window_interval) == 0]
    end_index = start_index + window_duration*f_s
    end_index = end_index[end_index<=len(signal)]
    start_index = start_index[:len(end_index)]
    
    signal_segments = []
    time_segments = []
    for window in np.arange(len(start_index)):
        signal_segments.append(signal[start_index[window]:end_index[window]])
        time_segments.append(time_signal[start_index[window]:end_index[window]])
        
    return signal_segments, time_segments

def array_rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def divide_to_epochs(a, epoch_endindex, epoch_size, fs):
    win_size = fs*epoch_size
    sig_epochs = [a[x-win_size +1 : x+1] for x in epoch_endindex]
    return np.vstack(sig_epochs)

def heart_rate(time_peaks):
    dt = time_peaks[1:] - time_peaks[:-1]
    return 1/np.nanmean(dt)

def heart_rate_var(time_peaks):
    dt = time_peaks[1:] - time_peaks[:-1]
    return np.nanstd(dt)

def bio_signal_peak_detect(sig, fs, sigtype = 'resp'):
    signaltype = {'resp': fs/2*4, 'ecg': fs/2*2, 'bp': fs/2}
    max_peaks, min_peaks = peakdetect(sig, lookahead = signaltype[sigtype])
    max_peaks_idx, max_peaks_val = zip(*max_peaks)
    min_peaks_idx, min_peaks_val = zip(*min_peaks)
    
    return  max_peaks_idx, max_peaks_val, min_peaks_idx, min_peaks_val

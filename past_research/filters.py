from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter


"""Bandpass and lowpass filtering functions. """

def bandpass_filter(x, lowcut=10.0, highcut=25.0, samplingRate=50.0, order=5, Plot=True):
    nyq = 0.5 * samplingRate
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, x)
    if Plot:
        plt.figure(1, figsize=(20, 2))
        plt.plot(x, 'c-', label='z_raw',)
        plt.grid(True)
        plt.axis('tight')
        plt.legend(loc=1)

        plt.figure(2, figsize=(20, 2))
        plt.plot(y, label='Filtered signal (%g Hz)' % samplingRate)
        plt.xlabel('time (seconds)')
        plt.grid(True)
        plt.axis('tight')
        plt.legend(loc=1)
        plt.show()
        
    return y


def lowpass_filter(data, cutoff, fs, order=6):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    
    return y

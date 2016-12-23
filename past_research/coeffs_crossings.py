from __future__ import division
import numpy as np


"""
Contains funtions for computing the number of zero crossings and the
coefficients used in Cole, Oakley and Sadeh's sleep-wake detection methods.
"""

def zero_crossing(data, samplingRate=100.0):
    signs = np.sign(data)
    signs[signs == 0] = -1
    return len(np.where(np.diff(signs))[0])

def signal_cut(arr_, threshold=0.001): #0.01
    arr_ = np.array(arr_)
    thresholded_data = arr_ > threshold
    if len(thresholded_data) > 0:
        threshold_edges = np.convolve([1, -1], thresholded_data, mode='same')
        thresholded_edge_indices = np.where(threshold_edges==1)[0]
        res = len(thresholded_edge_indices)
    else:
        res = 0
    return res

def cole_scoring(elems):
    coeffs = [1.06, 0.54, 0.58, 0.76, 2.3, 0.74, 0.67]
    return 0.0033 * (np.dot(elems, coeffs)) 


def cole_scoring_rms(elems):
    coeffs = [404, 598, 326, 441, 1408, 508, 350]
    return 0.00001 * (np.dot(elems, coeffs)) 


def oakley_scoring(elems):
    coeffs = [0.04, 0.2, 2.0, 0.2, 0.04]
    return (np.dot(elems, coeffs))


def sadeh_scoring(elems):
    """Sadeh's scoring algorithm coefficients for the four most predictive measures.
    
    Parameter
    ----------
    elems: array_like, length (4)
    
    Return
    ----------
    probability of sleep
    """
    coeffs = [-0.065, -1.08, -0.056, -0.703]
    return 7.601 + (np.dot(elems, coeffs)) 



import numpy as np
from itertools import groupby

def accel_sleep(vertical, sample_rate=10, movement_threshold=.2, sleep_threshold=6000):
    """
    Accepts the vertical component of acceleration (often the Z-axis) and calculates
    periods of sleep and wake. Based on ESS algorithm from Borazio (2014). Expanded to
    use run length weighting and changed definition of movement
    
    Inputs
    ------
    vertical : array-like
        Acceleration axis aligned parallel to gravity
    sample_rate : int
        Sampling rate of source accelerometer
    movement_threshold : float
        Threshold for whether a frame of data had movement in it. Based on standard deviation.
    sleep_treshold : int
        Unit of analysis for sleep segments in number of readings. Often aroudn 10 minutes
        
    Returns
    -------
    sleep_indices : list
        List of lists containing periods of sleep and wake:
            - [0] : Start of segment index
            - [1] : End of segment index 
            - [2] : 'Sleep' if True, 'Awake' if False
    """
    #Standard deviation in one second windows and thresholded for small movements
    sleep_threshold /= sample_rate
    sigma = np.array([np.std(vertical[i:i+sample_rate]) for i in range(0, len(vertical)-sample_rate, sample_rate)])
    bool_sigma = sigma < .2
    
    #Find all segments of at least length sleep_threshold and count them as sleep
    start_index = -1
    sleep_indices = []
    while start_index <= len(bool_sigma):
        start_index += 1
            
        if not all(bool_sigma[start_index:start_index+sleep_threshold]):
            continue
        
        #Add awake segments and filter out small segments
        if not sleep_indices:
            sleep_indices.append([0, start_index, False])
        elif (start_index-sleep_indices[-1][1]) < (sleep_threshold//3):
            sleep_indices[-1][1] = start_index
        else:
            sleep_indices.append([sleep_indices[-1][1], start_index, False])
            
        for j in range(start_index+sleep_threshold, len(bool_sigma)):
            if bool_sigma[j]:
                continue
            else:
                sleep_indices.append([start_index, j, True])
                start_index = j
                break
        
        #Add last segment if not already handled
        if j == len(bool_sigma)-1:
            sleep_indices.append([start_index, j, True])
            break
    
    #Expand data by window size
    sleep_indices = [[row[0]*sample_rate, row[1]*sample_rate, row[2]] for row in sleep_indices]
    
    return sleep_indices

from itertools import groupby

def accel_sleep_weighted(vertical, sample_rate=10, movement_threshold=.2, sleep_threshold=6000, rl_threshold=.95):
    """
    Accepts the vertical component of acceleration (often the Z-axis) and calculates
    periods of sleep and wake. Based on ESS algorithm from Borazio (2014). Expanded to
    use run length weighting and changed definition of movement. Also included in this
    version is the ability to threshold sleep wake segments based on average run length.
    In most cases 'accel_sleep' will be equally accurate and much faster. It may bare out
    that using the threshold does increase accuracy once more data is available.
    
    Inputs
    ------
    vertical : array-like
        Acceleration axis aligned parallel to gravity
    sample_rate : int
        Sampling rate of source accelerometer
    movement_threshold : float
        Threshold for whether a frame of data had movement in it. Based on standard deviation.
    sleep_treshold : int
        Unit of analysis for sleep segments in number of readings. Often aroudn 10 minutes
    rl_threshold : float (0.0-1.0)
        Threshold on average run length score. Higher values predict more wake.
        
    Returns
    -------
    sleep_indices : list
        List of lists containing periods of sleep and wake:
            - [0] : Start of segment index
            - [1] : End of segment index 
            - [2] : 'Sleep' if True, 'Awake' if False
    """
    #Standard deviation in size of one second and thresholded
    sleep_threshold /= sample_rate
    sigma = np.array([np.std(vertical[i:i+sample_rate]) for i in range(0, len(vertical)-sample_rate, sample_rate)])
    bool_sigma = sigma < movement_threshold
    rl_sigma = [[key, sum(1 for i in group)] for key,group in groupby(bool_sigma)]
    
    #Find segments of 10 minutes and score based on run length weighting
    start_index = 0
    sleep_scores = []
    for i in range(len(rl_sigma)):
        segment = rl_sigma[start_index:i]
        segment_size = sum([pair[1] for pair in segment])

        if rl_sigma[i][1] > sleep_threshold:
            start_index = i+1
            arl = np.mean([pair[1] for pair in segment])
            segment_score = np.mean([(pair[1]/arl)*pair[0] for pair in segment])

            sleep_scores.extend([segment_score]*segment_size)
            sleep_scores.extend([int(test[i][0])]*test[i][1])

        elif segment_size > sleep_threshold:
            start_index = i
            arl = np.mean([pair[1] for pair in segment])
            segment_score = np.mean([(pair[1]/arl)*pair[0] for pair in segment])

            sleep_scores.extend([segment_score]*segment_size)
    
    #Treshold scores and filter out small segments
    bool_scores = np.array(sleep_scores) < rl_threshold
    rl_scores = [[key, sum(1 for i in group)] for key,group in groupby(bool_scores)]
    
    sleep_indices = []
    for pair in score_rl:

        if not sleep_indices:
            sleep_indices.append([0, pair[1], not pair[0]])
        elif pair[0] and (pair[1] < 180):
            sleep_indices[-1][1] += pair[1]
        else:
            last_index = sleep_indices[-1][1]
            sleep_indices.append([last_index, last_index+pair[1], not pair[0]])
            
    return sleep_indices

import numpy as np


def find_orientation_change(data, time, seconds=60, min_dist=5, min_mean_diff=1, min_duration=7):
    """
    Finds where the orientation of an axis changes in accelerometer data.

    Args
    ____

    data: float array
        Accelerometer data to be examined.

    time: array-like
        Array of time stamps associated with the accelerometer data.

    seconds: int
        Moving window at which the data will be checked for variance and mean orientation.

    min_dist: int
        The minimum number of seconds that an orientation change should be from another
        in order to be considered.

    min_mean_diff: int
        The minimum difference between the mean of the last orientation change and
        another to be considered.

    min_duration: int
        The minimum number of seconds between the previous orientation change and the
        current candidate.

    Returns
    ______

    changes: array-like
        A list where each entry is where the orientation begins and ends.
        e.g. [[0, 10], [13, 24], [52, 80],...]

    var_data: float array
        The windowed variance of the accelerometer data where the number of
        seconds is determined by the 'seconds' argument.

    mean_data: float array
        The windowed mean of the accelerometer data where the number of
        seconds is determined by the 'seconds' argument.

    t: float array
        The windowed time stamps of the accelerometer data.
    """
    # Get variance and mean data and the timestamps associated.
    var_data, t = get_windowed_var(data, time, seconds)
    mean_data = get_windowed_mean(data, time, seconds)[0]

    # List to store where the orientation changes take place.
    changes = []

    # Index variable to go through the variance data.
    i = 0

    # Maximum variance threshold for a datapoint to be considered as an
    # orientation change.
    var_thresh = 5

    # Variable to keep track of where the previous orientation change took
    # place.
    previous_change = 0

    # Variable to keep track of what the mean of the previous orientation
    # change was. Set arbitrarily high at the start.
    previous_mean = 1000

    # If variance at i is less than 1, mark as possible orientation change
    while i < len(var_data):
        # Check if this is far enough from the last change to count
        if var_data[i] < var_thresh and i >= previous_change + min_dist:
            # Check if the mean is far enough from the previous mean
            mean_diff = abs(previous_mean - mean_data[i])

            if mean_diff >= min_mean_diff:
                previous_mean = mean_data[i]
                j = find_window(var_data, i)
                if(abs(i-j) >= min_duration):
                    previous_change = j
                    changes.append([i*seconds, j*seconds])
                    i = j

        elif var_data[i] < var_thresh and abs(previous_mean - mean_data[i]) <= min_mean_diff:
            j = find_window(var_data, i)
            changes[-1][1] = j*seconds
            previous_change = j
            previous_mean = mean_data[i]

        i += 1

    return changes, var_data, mean_data, t


def get_windowed_var(data, time, window_sec):
    """
    Returns the windowed variance of the input data.

    Args
    ____

    data: float array
        The accelerometer data associated with a particular axis.

    time: float array
        An array of timestamps associated with the accelerometer data.

    window_sec: int
        How wide the moving window should be in seconds.

    Returns
    _______

    variances: float array
        An array of the windowed variances.

    times: float array
        The timestamps associated with the windowed variances.
    """
    # List of variances to return
    variances = []

    # List of associated timestampes to return
    times = []

    # Moving window in seconds
    window = window_sec*10

    # Number of times the window has moved
    window_num = 0

    # Where the window will start
    start = 0

    # While the window is within the length of the data, append the windowed
    # variance to variances for that window.
    while window < len(data):
        var = np.var(data[start:window])
        variances.append(var)
        times.append(window_sec*window_num)
        window_num += 1
        start = window
        window += window_sec*10

    return variances, times


def get_windowed_mean(data, time, window_sec):
    """
    Returns the windowed mean of the input data.

    Args
    ____

    data: float array
        The accelerometer data associated with a particular axis.

    time: float array
        An array of timestamps associated with the accelerometer data.

    window_sec: int
        How wide the moving window should be in seconds.

    Returns
    _______

    means: float array
        An array of the windowed means.

    times: float array
        The timestamps associated with the windowed variances.
    """
    # The windowed means to be returned.
    means = []

    # The associated timestamps to be returned.
    times = []

    # The number of seconds in the moving window.
    window = window_sec*10

    # Number of times the window has moved.
    window_num = 0

    # Where the window will start.
    start = 0

    # While the window is within the length of the data, append the windowed
    # mean to means.
    while window < len(data):
        mean = np.mean(data[start:window])
        means.append(mean)
        times.append(window_sec*window_num)
        window_num += 1
        start = window
        window += window_sec*10

    return means, times


def find_window(data, index):
    """
    Finds where the variance in the data is greater than 1 starting
    from a given index where the variance is less than 1.

    Arguments
    _________

    data: array-like
        windowed variance data of ECG or respiration.

    index: int
        Location in the windowed variance data where the windowed
        variance is less than 1.


    Returns
    _______

    i: int
        Location of where the windowed variance ceases to be less
        than 1.
    """
    for i in range(index, len(data)):
        if data[i] > 1:
            return i
    return i

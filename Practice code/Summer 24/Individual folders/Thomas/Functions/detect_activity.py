import numpy as np

def moving_avg(series, window):
    series_padded = np.append([np.NaN] * (window//2 - 1), np.append(np.array(series), [np.NaN] * (window//2 - 1)))

    result = []

    for n, _ in enumerate(series):
        result += [np.average(series_padded[n:n+window])]

    return result

# get a difference between each point and its successor in the series
def diff(series):
    return [series[n+1] - series[n] for n in range(len(series) - 1)] + [0]

# return a list of pairs (time_start, time_stop) for each bout of activity
# based on slope to find start and stop times
def detect_slope(series, times, cutoff = .25, avg_window = 30, avg_slope_window = 10):
    smoothed = moving_avg(series, avg_window)
    slopes = moving_avg(diff(smoothed), avg_slope_window)

    def detect(slope):
        if (slope > cutoff):
            return 1
        if (slope < -cutoff):
            return -1
        return 0
    
    DETECT = np.vectorize(detect)(slopes)

    pairs = [[times[0], times[0]]]

    for n, d in enumerate(diff(DETECT)):
        if d > 0:
            pairs.append([times[n], times[n]])
        if d < 0:
            pairs[-1][1] = times[n]

    return pairs
                
def detect_threshold(series, times, avg_window = 30):
    smoothed = moving_avg(series, avg_window)

    smoothed_filtered = np.nan_to_num(smoothed)
    mean = np.mean(smoothed_filtered)

    def detect(level):
        return int(level > mean)
    
    DETECT = np.vectorize(detect)(smoothed)

    pairs = [[times[0], times[0]]]

    for n, s in enumerate(diff(DETECT)):
        if s > 0:
            pairs.append([times[n], times[n]])
        if s < 0:
            pairs[-1][1] = times[n]

    return pairs
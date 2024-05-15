import numpy as np
import matplotlib.dates as dates
from datetime import datetime

def moving_avg(series, window):
    series_padded = np.append([np.NaN] * (window//2 - 1), np.append(np.array(series), [np.NaN] * (window//2 - 1)))

    result = []

    for n, _ in enumerate(series):
        result += [np.average(series_padded[n:n+window])]

    return result

# get a difference between each point and its successor in the series
def diff(series):
    return [series[n+1] - series[n] for n in range(len(series) - 1)] + [0]

# return a list of pairs [time_start, time_stop] for each bout of activity
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

# return a pair of lists ([start_times], [stop_times]) for the beginnings and ends of each bout of activity
# based on threshold (mean)    
def detect_threshold_endpoints(series: np.ndarray, times, avg_window = 30):
    smoothed = moving_avg(series, avg_window)

    smoothed_filtered = np.nan_to_num(smoothed)
    mean = np.mean(smoothed_filtered)

    is_active_series = smoothed_filtered > mean

    is_active_series_shiftedback = np.append(np.delete(is_active_series, [1]), False)

    starts = times[(is_active_series == False) & (is_active_series_shiftedback == True)]
    stops = times[(is_active_series == True) & (is_active_series_shiftedback == False)]

    return starts, stops

# return a series of boolean values telling whether the spider is active or not at any given time
# based on threshold (mean)
def detect_threshold_series(series: np.ndarray, avg_window = 30):
    smoothed = moving_avg(series, avg_window)

    smoothed_filtered = np.nan_to_num(smoothed)
    mean = np.mean(smoothed_filtered)

    is_active_series = smoothed_filtered > mean

    return is_active_series

def format_times(axs, format):
    for ax in axs:
        ax.xaxis.set_major_formatter(dates.DateFormatter(format))

def interpret_times(strs, format):
    return np.array([datetime.strptime(time, format) for time in strs])

def mean_length(pairs):
    length_sum = 0
    for pair in pairs:
        length_sum += (pair[1].timestamp() - pair[0].timestamp())

    return length_sum / len(pairs)
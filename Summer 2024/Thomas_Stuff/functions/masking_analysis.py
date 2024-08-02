import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from processing import process_file

def average_all_dfs(file_names):
    """
    Number of minutes since the last midnight.
    
    Parameters:
    file_names: list[str]
        A list of file names to process data from.

    Returns:
    average_all: Series
        Time series containing the average across all spiders, all days for each time point in the index.
    """
    all_dfs = [] # list of all dataframes containing the activity data to be used
    n_sections = 0 # total number of ZT days across all dataframes; need to know how many to average over

    for n, file_name in enumerate(file_names):
        df = process_file(file_name)

        df = df.loc[:, (df != 0).any(axis=0)] # remove any columns with no data (could be dead, inactive, empty spot, etc.)

        n_sections += -(len(df.index) // -1440) # add the number of days in the DF to the number of total sections
        all_dfs += [df]

    sections_array = np.zeros((1440, n_sections)) # 1440xN 2D array, will average across the sections axis
    i_section = 0 # iteration variable

    for df in all_dfs:
        light_on_times = df.index[(df['Light'] == 1) & (df['Light'].shift(1) == 0)] # light is ON and was just OFF
        
        spiders = df.drop(['Light', 'Day', 'Time'], axis=1) # get only the spider activity data from the dataframe
        combined = spiders.mean(axis=1) # average across every spider

        # separate into sections (ZT days)
        for on_time in light_on_times:
            section = combined[on_time : on_time + 1440] # get a 1-day section starting from the lights-on
            sections_array[:len(section), i_section] = section # add a row, which is the average across all spiders of that ZT day in the DF
            
            i_section += 1

    average_all = sections_array[:, :i_section].mean(axis=1) # average across all days

    result = pd.Series(average_all) # convert to make it easier to work with Pandas
    
    return result

def mins(time):
    """
    Number of minutes since the last midnight.
    
    Parameters:
    time: datetime

    Returns:
    mins: int 
    """
    if isinstance(time, pd.Series):
        return time.dt.hour * 60 + time.dt.minute
    else:
        return time.hour * 60 + time.minute

def get_first_lightson(df):
    """
    Gets the first time that the lights are on

    Parameters:
    df: pandas dataframe -- the dataframe to calculate for

    Returns:
    datetime
    """
    lights = df['Light']
    light_on_times = df.index[(lights == 1) & (lights.shift(1) == 0)]
    return df['Time'][light_on_times[0]]
    
def get_masking_bounds(df, window_length_mins=120):
    """
    Start and end of the light pulse window.
    
    Parameters:
    df: DataFrame
        Dataframe to find the window for. Must contain 'Time' and 'Light' columns.
    window_length_mins: int
        Approximate length of the light pulse; doesn't need to be exact

    Returns:
    (start: datetime, end: datetime)
        The beginning and end of the pulse period
    """
    times = df['Time']

    lights = df['Light']
    
    light_off_times = list(df['Time'][(lights == 0) & (lights.shift(1) == 1)])
    light_on_times = list(df['Time'][(lights == 1) & (lights.shift(1) == 0)])

    first_off = light_off_times[0]
    first_on = light_on_times[0]

    off_bound = max(light_off_times, key=lambda t: abs(mins(t) - mins(first_off)))
    on_bound = max(light_on_times, key=lambda t: abs(mins(t) - mins(first_on)))
    
    return sorted((off_bound, on_bound))

def calculate_spider_activity(df, start_time, duration_mins=60):
    """
    Get the average activity of each individual spider during the specified time window

    Parameters:
    df: pandas dataframe
        Dataframe to get activity data from. Must have the same columns as one returned from processing.process_file()
    start_time: datetime
        Start of the measurement period
    duration_mins: int
        Length of measurement period

    Returns:
    average_activity: Series
        Pandas series of activities. average_activity['Sp{n}'] = the average activity of spider n across the specified time period
    """
    start_time = pd.to_datetime(start_time)
    end_time = start_time + pd.Timedelta(minutes=duration_mins)

    # get the specified time window of the dataframe
    mask = (df['Time'] >= start_time) & (df['Time'] < end_time)
    df_filtered = df.loc[mask]

    spider_columns = [col for col in df.columns if col.startswith('Sp')] # filter out the names of only spider activity data columns

    average_activity = df_filtered[spider_columns].mean() # average across the time window for each spider
    return average_activity

def get_pulse_data(pulse_df, control_series, duration_mins=60, measure_start=0):
    """
    Get the relevant data from the given pulse group and control group data: start of the pulse, 
        control group mean activity during pulse, individual pulse group spider activity during pulse

    Parameters:
    pulse_df: DataFrame
        DataFrame to get activity data from. Must have the same columns as one returned from processing.process_file()
    control_series: Series
        Average activity of the control group across one ZT day. Each time point is the average of all control group spiders across all days.
    duration_mins: int
        Length of the measurement window
    measure_start: int
        Number of minutes after the pulse start to start measuring

    Returns:
    (pulse_start_zt_mins: int, control_avg: float, activities: Series)
        pulse_start_zt_mins -- start of the pulse in the ZT day, in minutes
        control_avg -- average activity of the control group during the measurement window
        activities -- average activity of each individual pulse group spider during the measurement window
    """
    pulse_start = get_masking_bounds(pulse_df)[0]
    
    zt_start = get_first_lightson(pulse_df)

    pulse_start_zt_mins = int((pulse_start - zt_start).total_seconds() // 60) % 1440

    activities = calculate_spider_activity(pulse_df, pulse_start, duration_mins)

    control_avg = control_series[pulse_start_zt_mins : pulse_start_zt_mins + duration_mins].mean()

    return pulse_start_zt_mins, control_avg, activities

def mean_activity_across_pulse(pulse_df, control_series, window_size=10):
    """
    Get the activity in each interval across the duration of the light or dark pulse.

    Parameters:
    pulse_df: DataFrame
        DataFrame to get activity data from. Must have the same columns as one returned from processing.process_file()
    control_series: Series
        Average activity of the control group across one ZT day. Each time point is the average of all control group spiders across all days.
    window_size: int
        Size of the intervals to measure over

    Returns:
    points: Series
        Series of average activities of pulse group spiders across the duration of the pulse. Index: [0, window_size, ... 120)
    """
    measure_starts = np.arange(0, 120, window_size)
    points = []
    starts = []
    pulse_start = 0
    for start in measure_starts:
        pulse_start, _, activities = get_pulse_data(pulse_df, control_series, window_size, start)
        points.append(activities.mean())

    return pd.Series(points, index=measure_starts)
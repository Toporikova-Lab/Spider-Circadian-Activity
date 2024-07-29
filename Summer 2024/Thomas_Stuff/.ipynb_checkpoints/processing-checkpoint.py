import pandas as pd

def process_file(file):
    col_names = ["Index", "DateD", "DateM", "DateY", "Time", "MonStatus", "Extras", "MonN", "TubeN", "DataType", "Unused", "Light"]
    
    for i in range(1, 33):
        col_names.append(f"Sp{i}")
    
    df = pd.read_csv(file, names=col_names, sep='\s+', header=None)
    df = df.set_index('Index')
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
    df = df[df["MonStatus"] == 1]

    month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    df['DateM'] = df['DateM'].str[:3].map(month_map)
    df['DateY'] = df['DateY'].apply(lambda x: int(str(20) + str(x)))
    df['Date'] = pd.to_datetime(dict(year=df['DateY'], month=df['DateM'], day=df['DateD']), errors='coerce')

    df['Time'] = pd.to_datetime(dict(year=df['Date'].dt.year,
                                     month=df['Date'].dt.month,
                                     day=df['Date'].dt.day,
                                     hour=df['Time'].dt.hour,
                                     minute=df['Time'].dt.minute,
                                     second=df['Time'].dt.second))

    df = df.drop(["DateD", "DateM", "DateY", "Date", "MonStatus", "Extras", "MonN", "TubeN", "DataType", "Unused"], axis=1)

    day_map = {day: idx+1 for idx, day in enumerate(df['Time'].dt.day.unique())}

    df.insert(0, 'Day', df['Time'].dt.day.map(day_map))
    
    return df

def mins(time):
    if isinstance(time, pd.Series):
        return time.dt.hour * 60 + time.dt.minute
    else:
        return time.hour * 60 + time.minute

 def get_masking_bounds(df, window_length_mins = 120):
    times = df['Time']
    
    lights = df['Light']
    
    light_off_times = list(df['Time'][(lights == 0) & (lights.shift(1) == 1)])
    light_on_times = list(df['Time'][(lights == 1) & (lights.shift(1) == 0)])

    first_off = light_off_times[0]
    first_on = light_on_times[0]

    off_bound = max(light_off_times, key=lambda t: abs(mins(t) - mins(first_off)))
    on_bound = max(light_on_times, key=lambda t: abs(mins(t) - mins(first_on)))
    
    return sorted((off_bound, on_bound))

# get the average activity of each individual spider during the specified time window
# returns a pd.Series<float> with index Sp1, Sp2...Sp32
def calculate_spider_activity(df, start_time, duration_mins=60):
    start_time = pd.to_datetime(start_time)
    end_time = start_time + pd.Timedelta(minutes=duration_mins)

    # get the specified time window of the dataframe
    mask = (df['Time'] >= start_time) & (df['Time'] < end_time)
    df_filtered = df.loc[mask]

    spider_columns = [col for col in df.columns if col.startswith('Sp')] # filter out the names of only spider activity data columns

    average_activity = df_filtered[spider_columns].mean() # average across the time window for each spider
    return average_activity

# get the first time that the lights turn on
# returns a pd.Timestamp
def get_first_lightson(df):
    lights = df['Light']
    light_on_times = df.index[(lights == 1) & (lights.shift(1) == 0)]
    return df['Time'][light_on_times[0]]

# get all the relevant data from given pulse group and control group files: start of the pulse, control group mean activity during pulse, individual pulse group spider activity during pulse
# control_series must be a time series like one returned from average_all_dfs
# returns a 3-tuple (integer, float, pd.Series<float>)
def get_masking_data(pulse_file, control_series, duration_mins=60):
    pulse_df = process_file(pulse_file)
    pulse_start = get_masking_bounds(pulse_df)[0]
    
    zt_start = get_first_lightson(pulse_df)

    pulse_start_zt_mins = int((pulse_start - zt_start).total_seconds() // 60) % 1440

    activities = calculate_spider_activity(pulse_df, pulse_start, duration_mins)

    control_avg = control_series[pulse_start_zt_mins : pulse_start_zt_mins + duration_mins].mean()

    return pulse_start_zt_mins, control_avg, activities
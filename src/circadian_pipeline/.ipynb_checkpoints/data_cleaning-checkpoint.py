"""A module to prepare the raw CSV files 
of time series spider activity data for processing.

The data cleaning function accepts a CSV file and returns a list of the 
numbers of spiders included and a Pandas
Dataframe containing:
* An index value for each time series entry (sampled per minute)
* The day of the experiment each time value is associated with (indexed by 1)
* A DateTime value for each minute
* A column indicating whether the light is on (1) or off (0)
* A column for each spider documenting the number of activity counts at the given minute

Parameters
"""
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import datetime
import os

def data_organizer(file_name):

    col_names = ["Index", "DateD", "DateM", "DateY", "Time", "MonStatus", "Extras", "MonN", "TubeN", "DataType", "Unused", "Light"]
    
    for i in range(1, 33):
        col_names.append(f"Sp{i:02d}")
    
    folder_path = 'Data'
    file_path = os.path.join(folder_path, file_name)
    
    df = pd.read_csv(file_path, names=col_names, sep='\s+', header=None)
    df = df.set_index('Index')
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
      
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
    
    spiders = []
    
    for i in range(1, 33):
        if df[f"Sp{i:02d}"].sum() > 10:
            spiders.append(i)
        if not i in spiders:
            df = df.drop([f"Sp{i:02d}"], axis=1)

    return df, spiders

def get_deleted_data(df) :
    deleted_data = df[df["MonStatus"] != 1]
    num_rows = len(deleted_data)
    df = df[df["MonStatus"] == 1]
    return num_rows, deleted_data, df


def light_code(df):
    LL_days = []
    LD_days = []
    
    for j in range(1, len(df['Day'].unique()) + 1):
        curr_df = df[df['Day']==j]
    
        if curr_df['Light'].sum() > 10:
            if curr_df['Light'].sum() > 1000:
                LL_days.append(j)
            else:
                LD_days.append(j)
    
    condition_days = {}
    
    condition_days['LD'] = LD_days
    
    condition_days['DD'] = [x for x in df['Day'].unique() if not x in LL_days and not x in LD_days]
    
    condition_days['LL'] = LL_days
    
    
    condition_keys = [key for key in condition_days if condition_days[key]]

    return condition_days, condition_keys

def info_from_naming_pattern(file_name):
    group_name = file_name.split(' ', 2)[0]
    light_condition = file_name.split(' ', 2)[1]
    start_date = file_name.split(' ', 2)[2].split('-', 1)[0]
    
    path = group_name + "_" + light_condition + "_" + start_date
    
    two_lights = False
    if "-" in light_condition:
        two_lights = True

    return group_name, light_condition, start_date, path, two_lights

def resample_df_six_mins(df, spiders, binarize = False):
    df_res = df.copy()
    df_res.set_index('Time', inplace=True)

    spider_columns = [f"Sp{sp:02d}" for sp in spiders]

    df_resampled = df_res[spider_columns].resample('6T').sum()

    day_resampled = df_res['Day'].resample('6T').bfill()
    light_resampled = df_res['Light'].resample('6T').bfill()

    #if binarize = True, binarize dataframe
    if binarize:
        df_binary = df_resampled[spider_columns].map(convert_to_one)
        df_binary.insert(0, "Day", day_resampled)
        df_binary.insert(1, "Light", light_resampled)
        return df_binary
    else:
        df_resampled.insert(0, "Day", day_resampled)
        df_resampled.insert(1, "Light", light_resampled)
        return df_resampled


def convert_to_one(x):
    return 1 if x != 0 else 0
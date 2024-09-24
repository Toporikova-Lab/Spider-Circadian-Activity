"""
A module to prepare the raw CSV files 
of time series spider activity data for processing.

The data cleaning function accepts a txt or a CSV file and returns a list of the 
numbers of spiders included and a Pandas
Dataframe containing:
* An index value for each time series entry (sampled per minute)
* The day of the experiment each time value is associated with (indexed by 1)
* A DateTime value for each minute
* A column indicating whether the light is on (1) or off (0)
* A column for each spider documenting the number of activity counts at the given minute

Parameters
"""
import pandas as pd # Importing everything necessary for the functions
import numpy as np 
import matplotlib.pyplot as plt
import datetime
import os

def data_organizer(file_name, logbook_file=None):
    """
    This function takes in a file, creates a dataframe, organizes it, and returns the organized 
    Pandas dataframe and the numbers of the channels of the experimental subjects
    """

    if not logbook_file:
        logbook_df = pd.read_csv(logbook_file, header=1)
        logbook_sp_names = []
        
        for index, row in logbook_df.iterrows():
            logbook_sp_names.append(f"{row['Spider type']}{row['Spider ID']}_C{row["Channel"]:d02}")

        logbook_df['Spider Name'] = logbook_sp_names

        logbook_channels = logbook_df['Channel'].tolist()
        logbook_df.set_index('Channel', inplace=True)
        logbook_groups = logbook_df["Spider type"].unique()

    col_names = ["Index", "DateD", "DateM", "DateY", "Time", "MonStatus", "Extras", "MonN", "TubeN", "DataType", "Unused", "Light"]
    # These are the original columns in the DAM System monitors
    
    logbook_spiders = []

    for i in range(1, 33):
        if i in logbook_channels:
            logbook_spiders.append(logbook_df.loc[i, 'Spider Name'])
        else:
            logbook_spiders.append(f"Sp{i:02d}")
    # Creating columns for each spider
            
    col_names += logbook_spiders
    
    folder_path = 'Data'
    file_path = os.path.join(folder_path, file_name)
    # Opening the given file which is located in a folder called "Data"
    
    df = pd.read_csv(file_path, names=col_names, sep='\s+', header=None)
    df = df.set_index('Index')
    # Reading the original file into a dataframe, assigning the previously created column names
    # The original file does not have any column names
    
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
    # Changing the format of the "Time" column, so that it can be integrated into the "datetime" module
      
    month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    # The month map is needed to translate the string output of the monitor to a number, which can be used by the "datetime" module

    df['DateM'] = df['DateM'].str[:3].map(month_map)
    df['DateY'] = df['DateY'].apply(lambda x: int(str(20) + str(x)))
    # Translating the month and year into the values appropriate for the "datetime" module
    # Note: The function assumes the data is from year 2000 or later

    df['Date'] = pd.to_datetime(dict(year=df['DateY'], month=df['DateM'], day=df['DateD']), errors='coerce')
    # Creating a "Date" column which uses the translated year, month, and day
    
    df['Time'] = pd.to_datetime(dict(year=df['Date'].dt.year,
                                         month=df['Date'].dt.month,
                                         day=df['Date'].dt.day,
                                         hour=df['Time'].dt.hour,
                                         minute=df['Time'].dt.minute,
                                         second=df['Time'].dt.second))
    # Combining the "Time" and "Date" columns to create a new "Time" column, which has the exact time to minute in the "datetime" module
    
    df = df.drop(["DateD", "DateM", "DateY", "Date", "MonStatus", "Extras", "MonN", "TubeN", "DataType", "Unused"], axis=1)
    # Removing the columns in the dataframe that are not needed for further analysis
    
    day_map = {day: idx+1 for idx, day in enumerate(df['Time'].dt.day.unique())}
    df.insert(0, 'Day', df['Time'].dt.day.map(day_map))
    # Converting the date into experiment day and adding a new column named "Day"

    for name in logbook_spiders:
        if df[name].sum() < 10:
            df = df.drop([name], axis=1)

   
    """ Code without logbook
    spiders = []
    
    for i in range(1, 33):
        if df[f"Sp{i:02d}"].sum() > 10:
            spiders.append(i)
        if not i in spiders:
            df = df.drop([f"Sp{i:02d}"], axis=1)

    """

    # Excluding the channels that do not show more than 10 activity counts
    # 10 count cutoff aims to disregard the noise during the experiment setup
    # Creating a list of spiders that show activity in the experiment

    return df, logbook_spiders
    # The function returns the dataframe and the channel numbers of the subjects

def get_deleted_data(df) :
    """
    Finding the times when the monitor was not functional and removing these rows for cleaner data.
    Additionally, reporting to the user how many minutes of data were lost
    """
    deleted_data = df[df["MonStatus"] != 1]
    num_rows = len(deleted_data)
    df = df[df["MonStatus"] == 1]
    return num_rows, deleted_data, df


def light_code(df):
    """
    This function uses the information from "Light" column
    to determine whether each day of the experiment is DD, LD,
    or LL. Then, it returns the list of the present light 
    conditions and the days when each light condition takes place
    
    """
    LL_days = []
    LD_days = []
    
    for j in range(1, len(df['Day'].unique()) + 1):
        curr_df = df[df['Day']==j]
    
        if curr_df['Light'].sum() > 10:
            if curr_df['Light'].sum() > 1000:
                LL_days.append(j)
            else:
                LD_days.append(j)
    # Determining which days of the experiment have light and separating
    # them into LD and LL days based on the minutes of light on
    # 10 counts in determining an LD day were chosen in order to avoid
    # noise during experimental setup
    # 1000 counts in determining an LL day were chosen since most of the
    # time LD is about 12 hours (720 minutes), and 1000 is just in case

    condition_days = {}
    
    condition_days['LD'] = LD_days
    
    condition_days['DD'] = [x for x in df['Day'].unique() if not x in LL_days and not x in LD_days]
    
    condition_days['LL'] = LL_days
    # Creating a dictionary which contains the three light condition
    # possibilities and their corresponding days in the experiment
    
    condition_keys = [key for key in condition_days if condition_days[key]]
    # Determining which light conditions are present in the experiment

    return condition_days, condition_keys
    # This function returns the light conditions in the experiment
    # and the days of each light condition

def info_from_naming_pattern(file_name):
    """
    This function takes in a file name in the format
    of "group name + light condition + start date +
    end date + year", as follows

    Example: MsB LD-DD 0607 - 0618 - 2024.txt

    Then it creates a naming pattern for folders and files,
    so that it is easier to navigate the output of
    graphs from later functions
    """

    group_name = file_name.split(' ', 2)[0]
    light_condition = file_name.split(' ', 2)[1]
    start_date = file_name.split(' ', 2)[2].split('-', 1)[0]
    end_date = file_name.split(' ', 7)[4]
    # The function uses the naming pattern of the original file
    # to determine the group name, light condition(s), start date,
    # and end date of the experiment

    path = group_name + "_" + light_condition + "_" + end_date
    # The path combines the group name, light condition, and
    # end date of the experiment
    # It is later used to create folders to store graphs in
    
    two_lights = False
    if "-" in light_condition:
        two_lights = True
    # Checking if there are multiple light conditions in
    # the experiment (ex: LD-DD)

    return group_name, light_condition, start_date, end_date, path, two_lights
    # The function returns the group name, experimental light conditions, 
    # start date, end date, the folder path, and whether there are two
    # light conditions in the experiment

def resample_df_six_mins(df, logbook_spiders, binarize = False):
    """
    This function resamples the data frame into 6 minute
    pieces, which helps to better visualize sparse data.
    Additionally, it allows the user to then binarize the
    resampled data
    """

    df_res = df.copy()
    df_res.set_index('Time', inplace=True)
    # Creating a new data frame to later resample

    ###spider_columns = [f"Sp{sp:02d}" for sp in spiders]
    # Figuring out which columns need to be resampled

    df_resampled = df_res[logbook_spiders].resample('6T').sum()
    #df_resampled = df_res[spider_columns].resample('6T').sum()
    # Resampling the spider columns for every 6 minutes,
    # adding up all the counts

    day_resampled = df_res['Day'].resample('6T').bfill()
    light_resampled = df_res['Light'].resample('6T').bfill()
    # Resampling the day and light columns by removing the
    # 5 rows below each time point


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
    # This function determines whether there is 
    # activity in the resampled piece, and then
    # binarizes it
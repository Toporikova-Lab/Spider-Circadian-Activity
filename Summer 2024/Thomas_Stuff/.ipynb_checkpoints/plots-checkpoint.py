import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def raster_binary(dataframe, spider_name, title, rolling_window=1):
    sp_df = dataframe[['Day', 'Time', 'Light', spider_name]]
    
    days = sp_df['Day'].unique()
    
    fig, axs = plt.subplots(len(days), 1)
    
    fig.suptitle(title)
    fig.supxlabel('Time (hrs)')
    fig.supylabel('Day')
    
    # Separate activity by day
    for day, ax in zip(days, axs):
        sp_day = sp_df[sp_df['Day'] == day]
        time = sp_day['Time'].dt.hour + sp_day['Time'].dt.minute / 60
        light = sp_day['Light']
        activity = sp_day[spider_name]
    
        ax.tick_params(left=False, bottom=False)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_xlim(0, 24)
        ax.set_ylim(0, 1)
    
        ax.set_ylabel(day, rotation='horizontal')

        ax.fill_between(time, 0, 1, where=light, alpha=.5, color='yellow')
        ax.fill_between(time, 0, 1, where=(activity.rolling(rolling_window).mean() > 0), alpha=1)
    
    axs[-1].set_xticks(np.arange(0, 25, 2))
    axs[-1].set_xticklabels(np.arange(0, 25, 2), rotation = 'horizontal')

    return fig, axs

def raster_line(dataframe, spider_name, title, rolling_window=1):
    sp_df = dataframe[['Day', 'Time', 'Light', spider_name]]
    
    days = sp_df['Day'].unique()
    
    fig, axs = plt.subplots(len(days), 1)
    
    fig.suptitle(title)
    fig.supxlabel('Time (hrs)')
    fig.supylabel('Day')
    
    # Separate activity by day
    for day, ax in zip(days, axs):
        sp_day = sp_df[sp_df['Day'] == day]
        time = sp_day['Time'].dt.hour + sp_day['Time'].dt.minute / 60
        light = sp_day['Light']
        activity = sp_day[spider_name]
    
        ax.tick_params(left=False, bottom=False)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_xlim(-0.5, 23.5)
        ax.set_ylim(0, 1)
    
        ax.set_ylabel(day, rotation='horizontal')

        ax.fill_between(time, 0, 1, where=light, alpha=.5, color='yellow')

        ax.plot(time, activity / max(activity), color='black')
    
    axs[-1].set_xticks(np.arange(0, 25, 2))
    axs[-1].set_xticklabels(np.arange(0, 25, 2), rotation = 'horizontal')

    return fig, axs

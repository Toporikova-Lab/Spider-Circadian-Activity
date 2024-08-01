import numpy as _np
import matplotlib.pyplot as _plt

def raster_binary(dataframe, spider_name, title, rolling_window=1):
    """
    Makes a binary raster plot with data from the specified spider.

    Parameters:
    dataframe: pandas dataframe -- The dataframe in which to look for the spider
    spider_name: str -- The name of the spider to plot the data of
    title: str -- The title of the final graph
    rolling_window: int -- The width in minutes of the window to use for a rolling average; applied before binarization (default 1)

    Returns:
    tuple (matplotlib figure, matplotlib axes)
    """
    sp_df = dataframe[['Day', 'Time', 'Light', spider_name]] # get the dataframe with only the requested spider's data
    
    days = sp_df['Day'].unique()
    
    fig, axs = _plt.subplots(len(days), 1)
    
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
    
    axs[-1].set_xticks(_np.arange(0, 25, 2))
    axs[-1].set_xticklabels(_np.arange(0, 25, 2), rotation = 'horizontal')

    return fig, axs

def raster_line(dataframe, spider_name, title, rolling_window=1):
    """
    Makes a line-graph raster plot with non-binarized data from the specified spider.

    Parameters:
    dataframe: pandas.DataFrame -- The dataframe in which to look for the spider
    spider_name: str -- The name of the spider to plot the data of
    title: str -- The title of the final graph
    rolling_window: int -- The width in minutes of the window to use for a rolling average (default 1)

    Returns:
    tuple (matplotlib figure, matplotlib axes)
    """
    sp_df = dataframe[['Day', 'Time', 'Light', spider_name]]
    
    days = sp_df['Day'].unique()
    
    fig, axs = _plt.subplots(len(days), 1)
    
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
    
    axs[-1].set_xticks(_np.arange(0, 25, 2))
    axs[-1].set_xticklabels(_np.arange(0, 25, 2), rotation = 'horizontal')

    return fig, axs

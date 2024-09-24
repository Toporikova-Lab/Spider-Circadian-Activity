import data_cleaning
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import matplotlib.image as mpimg
import math
import re

def raster_plot(df, spider_column, group_name, end_date, raster_path, condition_days, average_raster=False):
    
    fig23 = plt.figure(figsize=(6, 4))

    for j in range(1, len(df['Day'].unique()) + 1):

        curr_df = df[df['Day'] == j]

        ax = fig23.add_subplot(len(df['Day'].unique()), 1, j)
        ax.set_ylabel(j, rotation="horizontal", va="center", ha="right", fontsize=8)

        for k in range(len(curr_df) - 1):
            start_time = curr_df.index[k]
            end_time = curr_df.index[k + 1]
            if curr_df['Light'].iloc[k] == 1:
                ax.axvspan(start_time.hour + start_time.minute / 60, 
                           end_time.hour + end_time.minute / 60, 
                           color='yellow', alpha=0.3)

        ax.bar(curr_df.index.hour + curr_df.index.minute / 60, 
               curr_df[spider_column], width=0.05, align='center')

        ax.set_ylim(0, 1.1)
        ax.tick_params(left=False, bottom=False)
        ax.set_yticklabels([])
        ax.set_xlim(-0.5, 23.5)
        ax.set_xticklabels([])
        ax.set_xlabel("")

        if j == 1:
            ax.set_title(f"{group_name} {spider_column[-2:]}")

        if j == len(df["Day"].unique()):
            ax.set_xticks(np.arange(0, 25, 2))
            ax.set_xticklabels(np.arange(0, 25, 2), rotation='horizontal', fontsize=7)
            ax.set_xlabel('Time (hours)')

        if len(condition_days["LD"]) > 1 and average_raster==True:
            average_raster()
            

    file_path = os.path.join(raster_path, f"{group_name}_{spider_column[-2:]}_{end_date}_raster_plot.png")
    plt.savefig(file_path)
    plt.close(fig23)


def average_raster():
    pass

def combined_raster(raster_path, group_name, end_date, figsize=(15, 10)):
    """
    This function gets all the raster plots from a folder, 
    and then combines them into one image.
    
    Parameters:
    raster_path: the folder that was previously created to store raster plots
    figsize: Size of the figure (optional, default is (15, 15))
    """

    filenames = sorted(os.listdir(raster_path), key=lambda x: int(re.search(r'\d+', x).group()))
    images = [mpimg.imread(os.path.join(raster_path, filename)) for filename in filenames]


    n = len(images)
    
    ncols = math.ceil(math.sqrt(n))
    nrows = math.ceil(n / ncols)
    # Calculate the number of rows and columns for the subplots

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    
    if n > 1:
        axes = axes.flatten()
    else:
        axes = [axes]
    
    for i, image in enumerate(images):
        axes[i].imshow(image)
        axes[i].axis('off')
    
    for i in range(n, len(axes)):
        fig.delaxes(axes[i])
    # Remove any unused subplots

    plt.tight_layout()
    file_path = os.path.join(raster_path, f"{group_name}_all_rasters_{end_date}.png")
    plt.savefig(file_path)
    plt.close()
import data_cleaning
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def raster_plot(df, spider_column, group_name, start_date, raster_path):
    
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

    file_path = os.path.join(raster_path, f"{group_name}_{spider_column[-2:]}_{start_date}_raster_plot.png")
    plt.savefig(file_path)
    plt.close(fig23)

    


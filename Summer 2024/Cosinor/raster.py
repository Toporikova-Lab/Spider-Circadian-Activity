import data_reading


def light_code(df):
    LL_days = []
    LD_days = []
    
    for j in range(1, len(df['Day'].unique()) + 1):
        curr_df = df[df['Day']==j]
    
        if curr_df['Light'].sum() > 10:
            print(curr_df['Light'].sum())
            if curr_df['Light'].sum() > 1000:
                LL_days.append(j)
            else:
                LD_days.append(j)

    condition_days = {}
    
    condition_days['LD'] = LD_days
    
    condition_days['DD'] = [x for x in df['Day'].unique() if not x in LL_days and not x in LD_days]
    
    condition_days['LL'] = LL_days
    
    
    """
    if two_lights:
        name_wrong = li_con_1 == 
        
    if light_condition == 
    
    li_con_1, li_con_2
    """
    
    condition_keys = [key for key in condition_days if condition_days[key]]

    return condition_days, condition_keys

def raster_plot_2(sp, fig, light_con, condition_days):
    #Hourly
    for j in condition_days[light_con]:
        curr_df = df[df['Day']==j]

        curr_df_avg = curr_df.groupby(curr_df['Time'].dt.hour)[sp].mean()
    
        ax = fig.add_subplot(len(df['Day'].unique()), 1, j)
        ax.set_ylabel(f"Day {j}", rotation="horizontal", va="center", ha="right", fontsize=8)

        
        for k in range(0, len(curr_df) -1):
            start_time = curr_df['Time'].iloc[k]
            end_time = curr_df['Time'].iloc[k + 1]
            if curr_df['Light'].iloc[k] == 1:
                ax.axvspan(start_time.hour + start_time.minute / 60, end_time.hour + end_time.minute / 60, color='yellow', alpha=0.3)

        curr_df_avg.plot.bar(y = [sp], ax=ax)
        
        ax.set_ylim(0, 1)
        ax.legend().remove()
        ax.tick_params(left=False, bottom=False)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_xlim(-0.5, 23.5)
        ax.set_xlabel("")
        
        if j == condition_days[light_con][0]:
            ax.set_title(f"{group_name} {sp.split('p', 2)[1]}")
            #ax.text(0.5, 1.5, x, fontsize=12, horizontalalignment='center', transform=ax.transAxes)
            
        if j == len(df["Day"].unique()):
            ax.set_xticks(np.arange(0, 25, 2))
            ax.set_xticklabels(np.arange(0, 25, 2), rotation = 'horizontal', fontsize = 7)
            ax.set_xlabel('Time (hours)')
        

    """
    file_path = os.path.join(raster_path, f"{group_name}_{sp.split('p', 2)[1]}_{light_condition}_{start_date}_raster_plot.png")
    plt.savefig(file_path)
    """
    #plt.close()
    plt.show()

def raster_plot(sp, fig, light_con, condition_days):
    #By minute 
    for j in condition_days[light_con]:
        curr_df = df[df['Day']==j]

        #curr_df_avg = curr_df.groupby(curr_df['Time'].dt.hour)[sp].mean()
    
        ax = fig.add_subplot(len(df['Day'].unique()), 1, j)
        ax.set_ylabel(j, rotation="horizontal", va="center", ha="right", fontsize=8)

        
        for k in range(0, len(curr_df) -1):
            start_time = curr_df['Time'].iloc[k]
            end_time = curr_df['Time'].iloc[k + 1]
            if curr_df['Light'].iloc[k] == 1:
                ax.axvspan(start_time.hour * 60 + start_time.minute, end_time.hour * 60 + end_time.minute, color='yellow', alpha=0.3)

        curr_df.plot.bar(y = [sp], ax=ax)
        
        ax.set_ylim(0, 5)
        ax.legend().remove()
        ax.tick_params(left=False, bottom=False)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_xlim(-0.5, 1440.5)
        ax.set_xlabel("")
        
        if j == condition_days[light_con][0]:
            ax.set_title(f"{group_name} {sp.split('p', 2)[1]}")
            #ax.text(0.5, 1.5, x, fontsize=12, horizontalalignment='center', transform=ax.transAxes)
            
        if j == len(df["Day"].unique()):
            ax.set_xticks(np.arange(0, 25, 2))
            ax.set_xticklabels(np.arange(0, 25, 2), rotation = 'horizontal', fontsize = 7)
            ax.set_xlabel('Time (hours)')
        

    """
    file_path = os.path.join(raster_path, f"{group_name}_{sp.split('p', 2)[1]}_{light_condition}_{start_date}_raster_plot.png")
    plt.savefig(file_path)
    """
    #plt.close()
    plt.show()

raster_path = path + "_raster_plots"

if not os.path.exists(raster_path):
    os.makedirs(raster_path)
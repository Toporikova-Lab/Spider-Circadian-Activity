import data_cleaning
import raster 
import lomb_scargle
import sys
import pandas as pd
import os 

def main():
    #Process user input: filename for processing, whether the DF should be binarized, and what to do with LS data
    filename = str(sys.argv[1])
    binarized = bool(sys.argv[2])
    result_type_ls = str(sys.argv[3])

    #Create dataframe
    df, spiders = data_cleaning.data_organizer(filename)

    #Get information from the name of the csv file
    group_name, light_condition, start_date, path, two_lights = data_cleaning.info_from_naming_pattern(filename)
    condition_days, condition_keys = data_cleaning.light_code(df)

    #Resample data to pass into raster plot
    df_processed = data_cleaning.resample_df_six_mins(df, spiders, binarize = binarized)

    raster_path = path + "_raster_plots"
    LS_path = "LS_" + path

    if not os.path.exists(LS_path):
        os.makedirs(LS_path)

    if not os.path.exists(raster_path):
        os.makedirs(raster_path)

    #display(df_processed)
    filepath = f"{group_name}_{start_date}_LS_info.txt"
    """# Ensure 'Time' column is in datetime format
    if not np.issubdtype(df['Time'].dtype, np.datetime64):
        df_processed['Time'] = pd.to_datetime(df['Time'])
    
    # Set 'Time' as the index
    df.set_index('Time', inplace=True)"""

    with open(filepath, "w") as info_file:
        print(spiders)
        for i in spiders:
            spider_column = f"Sp{i:02d}"  # Create the correct column name
            print(spider_column)
            print(spider_column[-2:])
            raster.raster_plot(df_processed, spider_column, group_name, start_date, raster_path)
            period, fap = lomb_scargle.period_LS(df_processed, spider_column, light_condition, condition_days, group_name, info_file, LS_path, start_date, result_type=result_type_ls)


if __name__ == "__main__":
    main()
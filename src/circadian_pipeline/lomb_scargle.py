from astropy.timeseries import LombScargle 
from jdcal import gcal2jd
import numpy as np
import matplotlib.pyplot as plt
import os
# Importing everything needed


def datetime_to_jd(dt):
    year, month, day = dt.year, dt.month, dt.day
    hour, minute, second = dt.hour, dt.minute, dt.second
    _, jd = gcal2jd(year, month, day)
    jd += (hour + minute / 60 + second / 3600) / 24
    return jd

def period_LS(df, spider, light_con, condition_days, info_file, LS_path, end_date, result_type='value'):
    valid_result_types = ['value', 'display', 'save', 'dis+save']
    if result_type not in valid_result_types:
        print("The 'result_type' parameter only takes in 'value', 'display', 'save', 'dis+save'.")
        return None
    
    info_file.write(f"\n\nLomb-Scargle information for Spider {spider} in {light_con} \n")

    first_day = condition_days[light_con][0]
    last_day = condition_days[light_con][-1]
    
    curr_df = df[(df["Day"] >= first_day) & (df["Day"] <= last_day)]

    if curr_df[spider].sum() < 10:
        info_file.write(f"No activity detected in the {light_con} light condition")
        return 0, 0

    activity = np.array(curr_df[spider])
    time = curr_df.index.to_series().apply(datetime_to_jd)

    ls = LombScargle(time, activity)
    freq = np.linspace(0.5, 2, len(activity))
    power = ls.power(freq)
    
    max_power = np.max(power)
    max_freq = freq[np.argmax(power)]

    periods = 1 / freq * 24

    fap = ls.false_alarm_probability(max_power)

    diff = np.diff(power)
    local_maxima_indices = np.where(np.logical_and(diff[:-1] > 0, diff[1:] < 0))[0]
    
    local_maxima_freqs = freq[local_maxima_indices]
    
    sorted_indices = np.argsort(power[local_maxima_indices])[::-1]
    
    sorted_local_maxima_freqs = local_maxima_freqs[sorted_indices]

    # Handle cases with fewer than 3 local maxima
    num_peaks = min(3, len(sorted_local_maxima_freqs))
    periods_under_maxima = 24 / sorted_local_maxima_freqs[:num_peaks]

    info_file.write("\nPeriods under top local maxima frequencies:\n")
    for i, period in enumerate(periods_under_maxima, 1):
        info_file.write(f"{i}: {period}\n")

    # Fill in missing periods with None
    period1, period2, period3 = list(periods_under_maxima) + [None] * (3 - num_peaks)
    
    best_period = 1 / max_freq
    best_period *= 24
    info_file.write(f"The Lomb-Scargle approximation of the {light_con} period is {best_period} hours.\n")
    info_file.write(f"The False Alarm Probability for this prediction is: {fap}")
    

    if result_type != 'value':
        plt.figure(figsize=(10, 6))
        plt.plot(periods, power)
        print(f"Best period: {best_period}")
        print(f"Periods range: {min(periods)} to {max(periods)}")
        print(f"Power range: {min(power)} to {max(power)}")
    
        if 12 <= best_period <= 49:  # Check if best_period is within the plot range
            best_period_index = np.argmin(np.abs(periods - best_period))
            best_period_power = power[best_period_index]
            plt.scatter(best_period, best_period_power, s=75, c="red")
            print(f"Plotting red dot at ({best_period_power})")
        else:
            print(f"Best period {best_period} is outside the plot range (12-48)")
        
        plt.axhline(y=0.05, color='r')
        plt.xlabel('Period (hours)')
        plt.ylabel('Power')
        plt.xlim(12, 49)
        plt.xticks(np.arange(12, 50, 2))
        plt.title(f'Lomb-Scargle Periodogram for {spider[:-4]} in {light_con}')
        plt.ylim(0, max(power) * 1.1) #Sets the y-axis slightly above max_power
        
        if result_type == 'display':
            plt.show()

        elif result_type == 'save':
            file_path = os.path.join(LS_path, f"LS_{spider[:-4]}_{light_con}_{end_date}.png")
            plt.savefig(file_path)
            plt.close()

        else: # result_type == 'dis+save'
            file_path = os.path.join(LS_path, f"LS_{spider[:-4]}_{light_con}_{end_date}.png")
            plt.savefig(file_path)
            plt.show()

    return best_period, fap

"""def plot_periodogram(periods, power, period1, max_power, group_name, spider):
    plt.figure(figsize=(10, 6))
    plt.plot(periods, power)
    plt.scatter(period1, max_power, s=75, c="red")
    #plt.scatter(period2, max_power, s=75, c="red")
    plt.xlabel('Period (hours)')
    plt.ylabel('Power')
    plt.xlim(12, 36)
    plt.xticks(np.arange(12, 37, 2))
    plt.title(f'Lomb-Scargle Periodogram for {group_name} {spider.split[-1]}')"""
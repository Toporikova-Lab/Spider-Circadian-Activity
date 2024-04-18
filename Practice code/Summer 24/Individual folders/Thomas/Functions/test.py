import pandas as pd
import detect_activity as dt
from datetime import datetime

df = pd.read_csv('/workspaces/Spider-Circadian-Activity/Practice code/Summer 24/Individual folders/Thomas/Practice Notebooks/Practice 2/Practice 2_data2.csv')

spider2 = df['s2']
times = [datetime.strptime(time, '%d %H:%M:%S') for time in df["Time"]]

pairs = dt.detect_slope(spider2, times)

for [x, y] in pairs:
    print(x, y)
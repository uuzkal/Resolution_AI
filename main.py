import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


df = pd.read_csv('interview_test_locations.csv')

id_tag_arr = pd.unique(df["id_tag"])

def str2timestamp(df, timestamp_column_name):
    result = []
    timestamps = df[timestamp_column_name].values
    for index in range(len(timestamps)):
        date_time_str = timestamps[index]
        try:
            date_time_obj = datetime.strptime(date_time_str.split('+')[0], '%Y-%m-%d %H:%M:%S.%f')
        except:
            date_time_obj = datetime.strptime(date_time_str.split('+')[0], '%Y-%m-%d %H:%M:%S')
        result.append(date_time_obj)

    return result

for id_tag in id_tag_arr:
    df_temp = df[df["id_tag"] == id_tag]
    x = df_temp["x"].values
    y = df_temp["y"].values
    plt.figure()
    plt.grid(visible=True)
    plt.title('Equipment ID: ' + str(id_tag))
    plt.scatter(x, y, color='black')
    waiting = 0
    waiting_coordinates = []
    timestamps = str2timestamp(df_temp, 'createdate')
    for index in range(len(timestamps)-1):
        elapsed_time = timestamps[index + 1] - timestamps[index]
        if elapsed_time.total_seconds() >= 1:
            if abs(x[index] - x[index + 1]) <= 2 and abs(y[index] - y[index + 1]) <= 2:
                if waiting == 0:
                    waiting_coordinates.append((x[index], y[index]))
                waiting += 1
            else:
                waiting = 0

    plt.scatter(*zip(*np.array(waiting_coordinates, dtype="i, i")), color='red', s=waiting, alpha=0.5)

    plt.show()



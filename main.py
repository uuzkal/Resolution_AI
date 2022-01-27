import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


df = pd.read_csv('interview_test_locations.csv', parse_dates=["createdate"])
df = df.drop_duplicates(subset=["id_tag", "createdate"]) # readings with duplicate timestamps and id_tags are removed
df["YYYY-MM-DD"] = df["createdate"].map(pd.Timestamp.date) # adding an extra column for dates
df["HH:MM:SS"] = df["createdate"].map(pd.Timestamp.time) # adding and extra column for times
id_tag_arr = pd.unique(df["id_tag"])
dates_arr = pd.unique(df["YYYY-MM-DD"])
times_arr = df["HH:MM:SS"].values


for date in dates_arr:
    df_date = df[df["YYYY-MM-DD"] == date]
    for id_tag in id_tag_arr:
        df_temp = df_date[df_date["id_tag"] == id_tag]
        X = df_temp["x"].values
        Y = df_temp["y"].values
        if X.size > 0 and Y.size > 0:
            plt.figure()
            plt.grid(visible=True)
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title('Equipment ID: ' + str(id_tag) + ', Date: ' + str(date))
            plt.scatter(X, Y, color='black', s=10, label="readings") # plotting readings
            # print(f"X size: {X.size}, Y size: {Y.size}")

            if X.size > 1 and Y.size > 1:
                X_temp = df_temp["x"].values
                Y_temp = df_temp["y"].values
                times = df_temp["HH:MM:SS"].values
                X = []
                Y = []
                waiting_time = 0
                waiting_start = 0
                waiting_end = 0
                waiting_times = []
                recording = True
                for index in range(len(X_temp) - 1):
                    if X_temp[index + 1] == X_temp[index] and Y_temp[index + 1] == Y_temp[index]:
                        if recording:
                            X.append(X_temp[index])
                            Y.append(Y_temp[index])
                            waiting_start = times[index]
                            waiting_end = times[index + 1]
                            # print("Waiting started at: " + str(waiting_start))
                            recording = False
                    elif not(recording) or index == len(X_temp) - 1:
                        waiting_end = times[index]
                        try:
                            waiting_time = datetime.combine(date, waiting_end) - datetime.combine(date, waiting_start)
                            # print("Waiting ended at: " + str(waiting_end))
                            waiting_time = round(waiting_time.total_seconds())
                            # print(f"Total waiting time in seconds: {waiting_time}s")
                            waiting_times.append(str(waiting_time) + "s")
                            waiting_start = 0
                            waiting_end = 0
                        except:
                            # print("No delay detected")
                            waiting_end = 0
                        recording = True

                    waiting_time = 0

                if len(X) > 1 and len(Y) > 1:
                    plt.plot(X, Y, label="flow_tag") # plotting flows
                arrowprops = dict(arrowstyle="->", connectionstyle="angle, angleA=45, angleB=135")
                for x, y, wt in zip(X, Y, waiting_times):
                    plt.scatter(x, y, color='red', s=int(wt.split("s")[0])*2, alpha=0.5) # plotting stoppage locations
                    plt.annotate(text=wt, xy=(x, y), arrowprops=arrowprops) # plotting stoppage time of that location
            plt.legend(loc="upper left")
            plt.show()



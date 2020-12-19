import json 
import sys
from tqdm import tqdm
import numpy as np
from datetime import date, timedelta
import ast 
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib as mp
import collections


start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date 

delta = edate - sdate  

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]


cities = json.load(open("json_results/fac_loc_results.json"))

alarms = {}
locations = []
diff_values = []
links_alarmed = []

tot_alarms = 0

file_id = 0


for date in range(delta.days + 1):

    # "Calculate" what day is going to be looped through
    day = sdate + timedelta(days=date)

    print(day)
 
    for hour in hours:
        try:
            file = open("../traceroutes/" + str(day) + "/" + hour + "00/actual_rtt_sw_alarms")
        except FileNotFoundError:
            print('fnfe')

        alarm_file = json.load(file)
        

        # {"(53, 306)":[12.141,20.33833,6.57349],"(57, 53)":[3.94867,5.48933,1.22499],"(857, 18)":[2.21267,252.068,2.60434],"(18, 18)":[5.617,157.03133,0.55183]}

        for key, alarm in alarm_file.items():
            link = ast.literal_eval(key)
            link0 = str(link[0])
            link1 = str(link[1])

            diff_values.append((alarm[1] - alarm[0], link0, link1, str(day), hour, file_id))

            tot_alarms = tot_alarms + 1

            if (link0, link1) not in links_alarmed:
                    links_alarmed.append((link0, link1))

            try:
                near_end = cities[link0]["city"]
                far_end = cities[link1]["city"]

                if near_end != far_end:
                    locations.append(near_end)
                    locations.append(far_end)
                else:
                    locations.append(near_end)


            except KeyError:
                locations.append("others")

            if link0 in alarms:
                if link1 in alarms[link0]:
                    alarms[link0][link1].append(file_id)
                else: 
                    alarms[link0][link1] = [file_id]
            else: 
                alarms[link0] = {
                    link1: [file_id]
                }
            
        file.close()

        file_id = file_id + 1

#output_file = open("phase3_scripts/results/mse_values",'w')
#output_file.write(json.dumps(mse_values))
#output_file.close()

alarm_durations = {}

for src in alarms:
    for dest in alarms[src]:
        hour_counter = 0
        for alarm in alarms[src][dest]:
            if hour_counter == 0:
                prev_index = alarm
                hour_counter = hour_counter + 1
            elif (alarm - prev_index) == 1:
                hour_counter = hour_counter + 1
                prev_index = alarm
            else:
                if hour_counter in alarm_durations:
                    alarm_durations[hour_counter] = alarm_durations[hour_counter] + 1
                else:
                    alarm_durations[hour_counter] = 1
                prev_index = alarm
                hour_counter = 1

            if hour_counter == 11:
                print(src, dest)

        if hour_counter in alarm_durations:
            alarm_durations[hour_counter] = alarm_durations[hour_counter] + 1
        else:
            alarm_durations[hour_counter] = 1
    
alarm_durations[0] = 0
print(alarm_durations)
hours_values = sorted(list(alarm_durations.keys()))
probability = []
previous = 0
for times in hours_values:
    previous = previous + alarm_durations[times]/sum(alarm_durations.values())
    probability.append(previous)


print(hours_values)

plt.figure(figsize=(7,5))
plt.plot(hours_values,probability)
plt.title("Duration of RTT Alarms")
plt.xlabel("Alarm Duration (Hours)")
plt.ylabel("CDF")
plt.grid()
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.savefig("phase3_scripts/results/rtt_cdf_graph.png")






locations = collections.Counter(locations)

print(locations)

diff_values.sort(reverse = True)

#print(locations)

#print(mse_values)

#output_file = open("phase3_scripts/results/mse_values",'w')
#output_file.write(json.dumps(mse_values))
#output_file.close()

diff_values_list = []
fac_list = []

for i in np.arange(50):
    text = "TOP " + str(i + 1) + " : " + str(diff_values[i])
    print(text)
    diff_values_list.append(diff_values[i][0])
    fac_list.append(str((diff_values[i][1], diff_values[i][2])))

print("LINKS THAT REPORTED AN ALARM ", len(links_alarmed))
print("Total amount of alarms", tot_alarms)

fig, ax = plt.subplots(figsize=(7,5))

plt.title("Top 50 RTT Alarms")

plt.xlabel("Ranking")
plt.ylabel("RTT diff (ms)")

labels_1 = ['1'] + [None]*8

for x in np.arange(10, 50, 10):
    labels_1 = labels_1 + [str(x)] + [None]*9

labels_1 = labels_1 + ['50']

data_normalizer = mp.colors.Normalize()

color_map = mp.colors.LinearSegmentedColormap(
    "my_map",
    {
        "red": [(0, 1.0, 1.0),
                (1.0, .5, .5)],
        "green": [(0, 0.5, 0.5),
                  (1.0, 0, 0)],
        "blue": [(0, 0.50, 0.5),
                 (1.0, 0, 0)]
    }
)


x_ticks = np.arange(0, 50, 10)
x = np.arange(0, 50)
#ax.yaxis.set_major_formatter(formatter)
plt.bar(x, diff_values_list, color=color_map(data_normalizer(diff_values_list)))
plt.xticks(x, labels_1)
#plt.show()
plt.savefig("phase3_scripts/results/rtt_diff_graph.png")
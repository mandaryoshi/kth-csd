import json 
import sys
from tqdm import tqdm
import numpy as np
from datetime import date, timedelta
import ast 
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib as mp


start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date 

delta = edate - sdate  

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

alarms = {}
mse_values = []
red_alarms = 0
yellow_alarms = 0

file_id = 0


for date in range(delta.days + 1):

    # "Calculate" what day is going to be looped through
    day = sdate + timedelta(days=date)

    print(day)
 
    # For each hour, add to the fw_comp-dictionary the observed values and the expected usage values of each link with the 
    # "origin" as near-end facility
    # Also adding a list of alarms and r and p values to plot them over the observations
    for hour in hours:
        try:
            file = open("../traceroutes/" + str(day) + "/" + hour + "00/fw_filtered_alarms")
        except FileNotFoundError:
            file = open("../traceroutes/" + str(day) + "/" + hour + "00/fw_alarms")

        alarm_file = json.load(file)

        for alarm_type in alarm_file:
            for alarm in alarm_file[alarm_type]:
                #if alarm[1] != '58' and alarm[1] != '18':
                mse_values.append((alarm[3], alarm[0], alarm[1], str(day), hour, file_id))
                if alarm[0] in alarms:
                    if alarm[1] in alarms[alarm[0]]:
                        if alarm_type in alarms[alarm[0]][alarm[1]]:
                            alarms[alarm[0]][alarm[1]][alarm_type].append((alarm[0], alarm[1], alarm[2], alarm[3], alarm[4], file_id))
                            #mse_values.append((alarm[3], alarm[0], alarm[1], str(day), hour, file_id))
                            if alarm_type == "red_alarms":
                                red_alarms = red_alarms + 1
                            else:
                                yellow_alarms = yellow_alarms + 1
                        else:
                            alarms[alarm[0]][alarm[1]][alarm_type] = [(alarm[0], alarm[1], alarm[2], alarm[3], alarm[4], file_id)]
                            #mse_values.append((alarm[3], alarm[0], alarm[1], str(day), hour, file_id))
                            if alarm_type == "red_alarms":
                                red_alarms = red_alarms + 1
                            else:
                                yellow_alarms = yellow_alarms + 1
                    else: 
                        alarms[alarm[0]][alarm[1]] = {
                            alarm_type : [(alarm[0], alarm[1], alarm[2], alarm[3], alarm[4], file_id)]
                        }
                        #mse_values.append((alarm[3], alarm[0], alarm[1], str(day), hour, file_id))
                        if alarm_type == "red_alarms":
                            red_alarms = red_alarms + 1
                        else:
                            yellow_alarms = yellow_alarms + 1
                else: 
                    alarms[alarm[0]] = {
                        alarm[1]: {
                            alarm_type : [(alarm[0], alarm[1], alarm[2], alarm[3], alarm[4], file_id)]
                        }
                    }
                    #mse_values.append((alarm[3], alarm[0], alarm[1], str(day), hour, file_id))
                    if alarm_type == "red_alarms":
                        red_alarms = red_alarms + 1
                    else:
                        yellow_alarms = yellow_alarms + 1

        file.close()

        file_id = file_id + 1

#output_file = open("phase3_scripts/results/mse_values",'w')
#output_file.write(json.dumps(mse_values))
#output_file.close()

mse_values.sort(reverse = True)

print("NUMBER OF TOTAL YELLOW ALARMS", yellow_alarms)
print("NUMBER OF TOTAL RED ALARMS", red_alarms)

#print(mse_values)

#output_file = open("phase3_scripts/results/mse_values",'w')
#output_file.write(json.dumps(mse_values))
#output_file.close()

mse_values_list = []
fac_list = []

for i in np.arange(50):
    text = "TOP " + str(i + 1) + " : " + str(mse_values[i])
    print(text)
    mse_values_list.append(mse_values[i][0])
    fac_list.append(str((mse_values[i][1], mse_values[i][2])))

fig, ax = plt.subplots(figsize=(7,5))

plt.title("Top 50 Forwarding Alarms")

plt.xlabel("Ranking")
plt.ylabel("MSE")

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
plt.bar(x, mse_values_list, color=color_map(data_normalizer(mse_values_list)))
plt.xticks(x, labels_1)
#plt.show()
plt.savefig("phase3_scripts/results/fw_mse_graph.png")
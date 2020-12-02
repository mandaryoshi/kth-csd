import json 
import sys
from tqdm import tqdm
import numpy as np
import datetime as dt
import ast 
from math import sqrt

#sys.path.insert(0, '/mnt/d/Documents/IK2200HT201-IXP')

#Define wilson function to determine confidence interval
def wilson(p, n, z = 1.96):
    denominator = 1 + z**2/n
    centre_adjusted_probability = p + z*z / (2*n)
    adjusted_standard_deviation = sqrt((p*(1 - p) + z*z / (4*n)) / n)
    
    lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator

    return (round(lower_bound*n), round(upper_bound*n))

# Input the date and hour for forwarding model link monitoring
# Date format = 2020-10-20
# Hour format = 18
date = sys.argv[1]

print(date)

split_date = date.split('-')
sdate = dt.date(int(split_date[0]), int(split_date[1]), int(split_date[2]))   

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

days = [-7, -6, -5, -4, -3, -2, -1]

mse_dict = {}

#Looping through the past 24 hours to calculate the reference values
for date in tqdm(days):

    day = sdate + dt.timedelta(days= date)

    for h in hours: 
        path = "/home/csd/traceroutes/" + str(day) + "/" + h + "00/fw_alarms"

        file = open(path)
        alarms = json.load(file)

        for alarm in alarms["red_alarms"]:
            if alarm[0] in mse_dict:
                if alarm[1] in mse_dict[alarm[0]]:
                    mse_dict[alarm[0]][alarm[1]].append(alarm[4])
                else:
                     mse_dict[alarm[0]][alarm[1]] = [alarm[4]]
            else:
                mse_dict[alarm[0]] = {
                    alarm[1]: [alarm[4]]
                }

        file.close()

del_list=[]

for source in mse_dict:
    for dest in mse_dict[source]:
        if len(mse_dict[source][dest]) >= 10:
            sorted_mse = sorted(mse_dict[source][dest])
            normal_ref = np.median(mse_dict[source][dest])
            ranks = wilson(0.5,len(sorted_mse))
            interval = (sorted_mse[ranks[0]], sorted_mse[ranks[1]])

            mse_dict[source][dest] = {
                "lower_bound": interval[0],
                "median": normal_ref,
                "upper_bound":  interval[1]
            }
        else:
            del_list.append((source, dest))

for link in del_list:
    del mse_dict[link[0]][link[1]]

path = "/home/csd/IK2200HT201-IXP/json_results/fw_alarm_ref"
output_file = open(path,'w')
output_file.write(json.dumps(mse_dict))
output_file.close()
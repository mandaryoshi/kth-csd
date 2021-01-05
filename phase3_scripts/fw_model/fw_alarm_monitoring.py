import json 
import sys
from tqdm import tqdm
import numpy as np
import datetime as dt
import ast 
from math import sqrt
from colorama import Fore, Back, Style

sys.path.insert(0, '/mnt/d/Documents/IK2200HT201-IXP')

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
hour = sys.argv[2]



path1 = "../../json_results/fw_alarm_ref"
file1 = open(path1)
ref_alarms = json.load(file1)

# Path for the hour you are monitoring
path = "../../../traceroutes/" + date + "/" + hour + "00/fw_alarms"
file = open(path)
alarms = json.load(file)

out_alarms = {"red_alarms":[],"yellow_alarms": []}

if "red_alarms" in alarms:
    for alarm in alarms["red_alarms"]:
        if alarm[0] in ref_alarms:
            if alarm[1] in ref_alarms[alarm[0]]:
                if alarm[4] > ref_alarms[alarm[0]][alarm[1]]["upper_bound"]:
                    out_alarms["red_alarms"].append(alarm)
                elif alarm[4] < ref_alarms[alarm[0]][alarm[1]]["lower_bound"]:
                    out_alarms["yellow_alarms"].append(alarm)
                elif abs(alarm[2]) < 0.35:
                    out_alarms["yellow_alarms"].append(alarm)
                else:
                    out_alarms["red_alarms"].append(alarm)
            elif abs(alarm[2]) < 0.4:
                out_alarms["yellow_alarms"].append(alarm)
            else:
                out_alarms["red_alarms"].append(alarm)
        elif abs(alarm[2]) < 0.4:
            out_alarms["yellow_alarms"].append(alarm)
        else:
            out_alarms["red_alarms"].append(alarm)

    if len(alarms["red_alarms"]) > 1:
        for alarm in alarms["red_alarms"]:
            comp = alarm[4]/alarm[3]
            if comp < 0.3:
                if alarm in out_alarms["red_alarms"]:
                    out_alarms["red_alarms"].remove(alarm)
                if alarm not in out_alarms["yellow_alarms"]:
                    out_alarms["yellow_alarms"].append(alarm)
    
    print("********* DATE: " + date + " " + hour + ":00h *********")
    print("TOTAL ALARMS: " + str(len(alarms["red_alarms"])))
    print(Fore.RED + "RED ALARMS: " + str(len(out_alarms["red_alarms"])))
    print(Fore.YELLOW + "YELLOW ALARMS: " + str(len(out_alarms["yellow_alarms"])))
    print(Style.RESET_ALL)
    
path = "../../../traceroutes/" + date + "/" + hour + "00/fw_filtered_alarms"
output_file = open(path,'w')
output_file.write(json.dumps(out_alarms))
output_file.close()


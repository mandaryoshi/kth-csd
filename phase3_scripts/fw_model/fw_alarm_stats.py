import json 
import sys
from tqdm import tqdm
import numpy as np
from datetime import date, timedelta
import ast 
from math import sqrt


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

output_file = open("phase3_scripts/results/mse_values",'w')
output_file.write(json.dumps(mse_values))
output_file.close()

mse_values.sort(reverse = True)

print("NUMBER OF TOTAL YELLOW ALARMS", yellow_alarms)
print("NUMBER OF TOTAL RED ALARMS", red_alarms)

#print(mse_values)

#output_file = open("phase3_scripts/results/mse_values",'w')
#output_file.write(json.dumps(mse_values))
#output_file.close()

for i in np.arange(10):
    text = "TOP " + str(i + 1) + " : " + str(mse_values[i])
    print(text)

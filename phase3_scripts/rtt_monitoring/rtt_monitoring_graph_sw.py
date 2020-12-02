#This script is run to draw the graph that visualizes the rtt trend and alarm detections
import ujson 
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

#Use 24 hours a day for X-axis
hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

#Define start date and end date for the graph as input parameters        
start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

#Define source and destination links that want to monitor
source = sys.argv[3]
dest = sys.argv[4]

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date

delta = edate - sdate       # as timedelta

#Create lists for errorbar
normal_reference_upper = []     #initial reference upper_bound
normal_reference_median = []    #initial reference median
normal_reference_lower = []     #initial reference lower_bound

rtt_upper = []      #current upper_bound
rtt_median =  []    #current median
rtt_lower = []      #current lower_bound

date_list = []  #list of dates

for date in tqdm(range(delta.days + 1)):
    day = sdate + timedelta(days=date)   
    for hour in tqdm(hours):
        if hour == "00":
            date_list.append(str(day))
        else:
            date_list.append(hour) 
        #Open initial reference computation result
        file1 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_ref_values")
        rtt_ref_values = ujson.load(file1)
        key = str((int(source), int(dest)))
        #Append the value to each variable list
        if key in rtt_ref_values:
            normal_reference_upper.append(rtt_ref_values[key]["upper_bd"])
            normal_reference_lower.append(rtt_ref_values[key]["lower_bd"])
            normal_reference_median.append(rtt_ref_values[key]["median"])

            #Open current computation result
            file2 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_medians")
            rtt_medians = ujson.load(file2)
            
            #Append the value to each variable list
            rtt_upper.append(rtt_medians[key]["upper_bd"] - rtt_medians[key]["median"])
            rtt_lower.append(rtt_medians[key]["median"] - rtt_medians[key]["lower_bd"])
            rtt_median.append(rtt_medians[key]["median"])

            file3 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_alarms")
            alarms = ujson.load(file3)

            if key in alarms["alarms"]:
                alarm_list.append(len(date_list) -1)

            file2.close()
            file3.close()
        else:
            print("INVALID LINK")
            sys.exit()
        
        file1.close()

alarm_values = []
for index in alarm_list:
    alarm_values.append(rtt_median[index])

#start graphing

plt.figure(figsize=(30,10))

plt.xticks(np.arange(len(date_list)),date_list,rotation='vertical')

err_list = [rtt_lower, rtt_upper]

#Normal reference computation result
plt.plot(np.arange(len(date_list)), normal_reference_median, marker ='.', color = 'forestgreen')
#for x,y in zip(np.arange(216), normal_reference_median):
 #   label = y
 #   plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,10), ha='center') 

plt.fill_between(np.arange(len(date_list)), normal_reference_lower, normal_reference_upper, color='forestgreen', alpha=.1)

#Current computation result
plt.errorbar(np.arange(len(date_list)), rtt_median, yerr=err_list, fmt='.',color='thistle',capsize=5)
plt.plot(np.arange(len(date_list)), rtt_median, color='gold')

plt.scatter(alarm_list, alarm_values, marker='X', color='magenta')
#for x,y in zip(np.arange(216), rtt_median):
#    label = y
#    plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,10), ha='center') 
plt.xlabel("Date")
plt.ylabel("Differential RTT values")
plt.savefig('../results/rtt_sw_graph.png')



# Initial reference for sliding window method and 1ms threshold
import ujson 
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

#24 hour for a day refers to X axis
hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]
 
 #start date and end date for the graph as input parameter
start_date = sys.argv[1].split('-') 
end_date = sys.argv[2].split('-') 

#Source and destination link that will monitor
source = sys.argv[3] 
dest = sys.argv[4] 

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date

delta = edate - sdate       # as timedelta

#list of errorbar create
normal_reference_upper = []
normal_reference_median = []
normal_reference_lower = []

rtt_upper = [] #current upper_bound
rtt_median =  [] #current median
rtt_lower = [] #current lower_bound

alarm_list = [] #list of alarm
date_list = [] #list of date
actual_rtt_list = []

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

        file2 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_medians")
        rtt_medians = ujson.load(file2)
       
         #Add the value to each variable list
        key = str((int(source), int(dest)))
        
        if key in rtt_ref_values and key in rtt_medians:
            
            normal_reference_upper.append(rtt_ref_values[key]["upper_bd"])
            normal_reference_lower.append(rtt_ref_values[key]["lower_bd"])
            normal_reference_median.append(rtt_ref_values[key]["median"])

            #ref_intervallist.append([rtt_ref_values[key]["lower_bd"],rtt_ref_values[key]["upper_bd"]])

            #Add the value to each variable list
            
            rtt_upper.append(rtt_medians[key]["upper_bd"] - rtt_medians[key]["median"])
            rtt_lower.append(rtt_medians[key]["median"] - rtt_medians[key]["lower_bd"])
            rtt_median.append(rtt_medians[key]["median"])

            #rtt_intervallist.append([rtt_medians[key]["median"] - rtt_medians[key]["lower_bd"], rtt_medians[key]["upper_bd"] - rtt_medians[key]["median"]])
            #file3 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_alarms")
            #alarms = ujson.load(file3)

            file4 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/actual_rtt_sw_alarms")
            actual_rtts = ujson.load(file4)

            #if key in alarms["alarms"]:
            #    alarm_list.append(len(date_list) -1)

            if key in actual_rtts.keys():
                alarm_list.append(len(date_list) -1)
                actual_rtt_list.append(str(actual_rtts[key]))
                print(actual_rtt_list)
                from ast import literal_eval
                tup = literal_eval(actual_rtt_list)
                print(tup)
            file2.close()
            #file3.close()
            file4.close()
        else:
            print("INVALID LINK")
            sys.exit()
        
        file1.close()

alarm_values = []
#actual_rtt_values = []
for index in alarm_list:
    alarm_values.append(rtt_median[index])
    #actual_rtt_values.append()

#start graphing

plt.figure(figsize=(30,10))

plt.title("RTT Pattern for " + source + " - " + dest)

plt.xticks(np.arange(len(date_list)),date_list,rotation='vertical')

err_list = [rtt_lower, rtt_upper]

plt.plot(np.arange(len(date_list)), normal_reference_median, marker ='.', color='forestgreen')

plt.fill_between(np.arange(len(date_list)), normal_reference_lower, normal_reference_upper, color='forestgreen', alpha=.1)

plt.errorbar(np.arange(len(date_list)), rtt_median, yerr=err_list,fmt='.',color='darkorange',capsize=5)
plt.plot(np.arange(len(date_list)), rtt_median, color='orange') 

plt.scatter(alarm_list, alarm_values, marker='X', color='red')

for x,y in zip(alarm_list, actual_rtt_list):
    label = f"({y[0]},{y[1]})"
    plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel("Date")
plt.ylabel("Differential RTT values")
#plt.grid(True)
plt.savefig('../results/rtt_sw_graph.png')



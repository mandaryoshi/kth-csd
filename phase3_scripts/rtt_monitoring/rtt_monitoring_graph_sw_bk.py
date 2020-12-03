import ujson 
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]
         
start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

source = sys.argv[3]
dest = sys.argv[4]

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date

delta = edate - sdate       # as timedelta

normal_reference_upper = []
normal_reference_median = []
normal_reference_lower = []

rtt_upper = []
rtt_median =  []
rtt_lower = []

alarm_list = []
date_list = []

for date in tqdm(range(delta.days + 1)):
    day = sdate + timedelta(days=date)   
    for hour in tqdm(hours):
        if hour == "00":
            date_list.append(str(day))
        else:
            date_list.append(hour)
        
        file1 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_ref_values")
        rtt_ref_values = ujson.load(file1)

        file2 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_medians")
        rtt_medians = ujson.load(file2)
        
        key = str((int(source), int(dest)))
        
        if key in rtt_ref_values and key in rtt_medians:
            
            normal_reference_upper.append(rtt_ref_values[key]["upper_bd"])
            normal_reference_lower.append(rtt_ref_values[key]["lower_bd"])
            normal_reference_median.append(rtt_ref_values[key]["median"])

            #ref_intervallist.append([rtt_ref_values[key]["lower_bd"],rtt_ref_values[key]["upper_bd"]])

            
            
            rtt_upper.append(rtt_medians[key]["upper_bd"] - rtt_medians[key]["median"])
            rtt_lower.append(rtt_medians[key]["median"] - rtt_medians[key]["lower_bd"])
            rtt_median.append(rtt_medians[key]["median"])

            #rtt_intervallist.append([rtt_medians[key]["median"] - rtt_medians[key]["lower_bd"], rtt_medians[key]["upper_bd"] - rtt_medians[key]["median"]])
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

plt.title("RTT Pattern for " + source + " - " + dest)

plt.xticks(np.arange(len(date_list)),date_list,rotation='vertical')

err_list = [rtt_lower, rtt_upper]

plt.plot(np.arange(len(date_list)), normal_reference_median, marker ='.', color='forestgreen')


#for x,y in zip(np.arange(216), normal_reference_median):
 #   label = y
 #   plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,10), ha='center') 

plt.fill_between(np.arange(len(date_list)), normal_reference_lower, normal_reference_upper, color='forestgreen', alpha=.1)

plt.errorbar(np.arange(len(date_list)), rtt_median, yerr=err_list,fmt='.',color='darkorange',capsize=5)
plt.plot(np.arange(len(date_list)), rtt_median, color='orange') 


plt.scatter(alarm_list, alarm_values, marker='X', color='red')
#for x,y in zip(np.arange(216), rtt_median):
#    label = y
#    plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,10), ha='center') 
plt.xlabel("Date")
plt.ylabel("Differential RTT values")
#plt.grid(True)
plt.savefig('../results/rtt_sw_graph.png')



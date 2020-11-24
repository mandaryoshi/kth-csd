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
        key = str((int(source), int(dest)))
        if key in rtt_ref_values:
            normal_reference_upper.append(rtt_ref_values[key]["upper_bd"])
            normal_reference_lower.append(rtt_ref_values[key]["lower_bd"])
            normal_reference_median.append(rtt_ref_values[key]["median"])

            #ref_intervallist.append([rtt_ref_values[key]["lower_bd"],rtt_ref_values[key]["upper_bd"]])

            file2 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_medians")
            rtt_medians = ujson.load(file2)
            
            rtt_upper.append(rtt_medians[key]["upper_bd"] - rtt_medians[key]["median"])
            rtt_lower.append(rtt_medians[key]["median"] - rtt_medians[key]["lower_bd"])
            rtt_median.append(rtt_medians[key]["median"])

            #rtt_intervallist.append([rtt_medians[key]["median"] - rtt_medians[key]["lower_bd"], rtt_medians[key]["upper_bd"] - rtt_medians[key]["median"]])

            file2.close()
        else:
            print("INVALID LINK")
            sys.exit()
        
        file1.close()

#start graphing

plt.figure(figsize=(30,10))

plt.xticks(np.arange(168),date_list,rotation='vertical')

err_list = [rtt_lower, rtt_upper]

plt.plot(np.arange(168), normal_reference_median, marker ='s')
#for x,y in zip(np.arange(216), normal_reference_median):
 #   label = y
 #   plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,10), ha='center') 

plt.fill_between(np.arange(168), normal_reference_lower, normal_reference_upper, color='b', alpha=.1)

plt.errorbar(np.arange(168), rtt_median, yerr=err_list, fmt='o',capsize=5)
#for x,y in zip(np.arange(216), rtt_median):
#    label = y
#    plt.annotate(label, (x,y), textcoords="offset points", xytext=(0,10), ha='center') 
plt.xlabel("Date")
plt.ylabel("Differential RTT values")
plt.savefig('../results/rtt_sw_graph.png')



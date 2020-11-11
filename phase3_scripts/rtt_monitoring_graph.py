import ujson 
import sys
from tqdm import tqdm
import numpy as np
import scipy.stats as st
import time
import matplotlib.pyplot as plt
from datetime import date, timedelta

#results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_alarms"
#save_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_ref_values"
#results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_medians"
hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]
         
start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

source = sys.argv[3]
dest = sys.argv[4]

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date

delta = edate - sdate       # as timedelta

#print(sdate)
#print(edate)
#print(delta.days)

normal_reference_upper = []
normal_reference_median = []
normal_reference_lower = []

rtt_upper = []
rtt_median =  []
rtt_lower = []

date_list = []

rtt_intervallist = []

for date in tqdm(range(delta.days + 1)):
    day = sdate + timedelta(days=date)
    #print(day)
    #print(date)    
    for hour in tqdm(hours):
        if hour == "00":
            date_list.append(day)
        else:
            date_list.append(hour)
        file1 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_ref_values")
        rtt_ref_values = ujson.load(file1)
        key = str((int(source), int(dest)))
        if key in rtt_ref_values:
            normal_reference_upper.append(rtt_ref_values[key]["upper_bd"])
            normal_reference_lower.append(rtt_ref_values[key]["lower_bd"])
            normal_reference_median.append(rtt_ref_values[key]["median"])

            file2 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_medians")
            rtt_medians = ujson.load(file2)
            #rtt_upper.append(rtt_medians[key]["upper_bd"])
            #rtt_lower.append(rtt_medians[key]["lower_bd"])
            #rtt_median.append(rtt_medians[key]["median"])


            rtt_intervallist.append([rtt_medians[key]["lower_bd"],rtt_medians[key]["median"],rtt_medians[key]["upper_bd"]])

            file2.close()
        else:
            print("INVALID LINK")
            sys.exit()
        
        file1.close()
       
    #day = sdate + timedelta(days=date)
    #print(day)

#start graphing

plt.figure()

plt.boxplot(rtt_intervallist)
plt.plot(date_list)

plt.savefig('results/rtt_graph.png')


#plt.show()
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

sdate = date(start_date[0], start_date[1], start_date[2])   # start date
edate = date(end_date[0], end_date[1], end_date[2])   # end date

delta = edate - sdate       # as timedelta

normal_reference_upper = []
normal_reference_median = []
normal_reference_lower = []

rtt_upper = []
rtt_median =  []
rtt_lower = []



for date in tqdm(range(delta.days + 1)):
    
    for hour in tqdm(hours):

        file1 = open("/home/csd/traceroutes/" + date + "/" + hour + "/rtt_ref_values")
        rtt_ref_values = ujson.load(file1)

        if source in rtt_ref_values:
            if dest in rtt_ref_values[source]:
                normal_reference_upper.append(rtt_ref_values[source][dest]["upper_bd"])
                normal_reference_lower.append(rtt_ref_values[source][dest]["lower_bd"])
                normal_reference_median.append(rtt_ref_values[source][dest]["median"])

                file2 = open("/home/csd/traceroutes/" + date + "/" + hour + "/rtt_medians")
                rtt_medians = ujson.load(file2)
                rtt_upper.append(rtt_medians[source][dest]["upper_bd"])
                rtt_lower.append(rtt_medians[source][dest]["lower_bd"])
                rtt_median.append(rtt_medians[source][dest]["median"])

                file2.close()

            else:
                print("INVALID LINK")
                sys.exit()
        else:
            print("INVALID LINK")
            sys.exit()
        
        file1.close()
       
    day = sdate + timedelta(days=date)
    print(day)

print(len(normal_reference_upper))
print(len(normal_reference_lower))
print(len(normal_reference_median))


print(len(rtt_upper))
print(len(rtt_median))
print(len(rtt_lower))



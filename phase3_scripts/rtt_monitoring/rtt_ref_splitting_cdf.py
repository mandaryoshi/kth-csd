import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import time
from shutil import copyfile
from datetime import date, timedelta


start_date = sys.argv[1].split('-') 
end_date = sys.argv[2].split('-') 

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date
delta = edate - sdate       # as timedelta

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

#path for fetching the reference values
for date in range(delta.days + 1):
    day = sdate + timedelta(days=date)   
    for hour in hours:      
        file1 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_ref_values")
        rtt_ref_values = ujson.load(file1)
        rtt_ref_links = dict.fromkeys(rtt_ref_values.keys()) 
   
print(rtt_ref_links)
print(len(rtt_ref_links))
for item in rtt_ref_links.keys():
    if rtt_ref_links[item] == None:
        rtt_ref_links[item] = 0
        
print(rtt_ref_links)

count = 0
#create a dictionary nd value wil be 0
for date in range(delta.days + 1):
    day = sdate + timedelta(days=date)   
    for hour in hours:
        file2 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/rtt_sw_alarms")
        rtt_ref_alarms = ujson.load(file2)
        for item in rtt_ref_alarms["alarms"]:
            if item in rtt_ref_links.items():
                rtt_ref_links[item] = count+1 
    

print(rtt_ref_links)
print(len(rtt_ref_links))

'''



for link in ref.keys():
    if link in links and len(links[link]["rtts"]) > 5:
        sorted_rtts = sorted(links[link]["rtts"])
        normal_ref = np.median(sorted_rtts)
        ranks = wilson(0.5,len(sorted_rtts))
        #print(ranks, len(sorted_rtts))
        interval = (round(sorted_rtts[ranks[0]],5), round(sorted_rtts[ranks[1]],5))
        ref_interval = (ref[link]["lower_bd"],ref[link]["upper_bd"])
        if (((interval[0] - ref_interval[1]) > ref[link]["diff"]) or  ((ref_interval[0] - interval[1]) > ref[link]["diff"])):
            #currnt_lb - ref_ub or ref_lb - curr_ub
            #print("Alarm triggered!!", link, interval, ref_interval)
            alarm_dict["alarms"].append(link)

        median_dict[link] = {
            "lower_bd" : interval[0],
            "median" : normal_ref,
            "upper_bd" : interval[1]
        }


ref_file.close()
results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_medians"
with open(results_path, 'w') as fp:
    ujson.dump(median_dict, fp)

fp.close()

results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_alarms"
with open(results_path, 'w') as fp:
    ujson.dump(alarm_dict, fp)

fp.close()

print(date, hour)'''

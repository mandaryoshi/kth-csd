import ujson 
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import ast 

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]
         
start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

origin = sys.argv[3]
#dest = sys.argv[4]

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date

delta = edate - sdate       # as timedelta

date_list = []

fw_comp_model = {}

for date in tqdm(range(delta.days + 1)):
    day = sdate + timedelta(days=date)
 
    
    for hour in tqdm(hours):
        if hour == "00":
            date_list.append(str(day))
        else:
            date_list.append(hour)
        file1 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/fw_model_comparison")
        new_model = ujson.load(file1)

        file2 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/fw_alarms")
        alarms = ujson.load(file2)
        ### {1: {2:[40,50]}, {3:[40,50]}, {5:[40,0]}, {10:[0,40]}} ###
        for source in new_model:
            for dest, value in new_model[source].items():
                if source in fw_comp_model:
                    if dest in fw_comp_model[source]:
                        fw_comp_model[source][dest]["ref"].append(value[0])
                        if len(value) == 1:
                            fw_comp_model[source][dest]["obs"].append(0)
                        else:
                            fw_comp_model[source][dest]["obs"].append(value[1])
                    else:
                        fw_comp_model[source][dest] = {"ref" : [value[0]]}
                        if len(value) == 1:
                            fw_comp_model[source][dest]["obs"] = [0]
                        else:
                            fw_comp_model[source][dest]["obs"] = [value[1]]       
                else:
                    fw_comp_model[source] = {dest : {"ref" : [value[0]]}}
                    if len(value) == 1:
                        fw_comp_model[source][dest]["obs"] = [0]
                    else:
                        fw_comp_model[source][dest]["obs"] = [value[1]]
        file1.close()
        for key in alarms["alarms"]:
            link0 = key[0]
            link1 = key[1]
            if link0 in fw_comp_model:
                if link1 in fw_comp_model[link0]:
                    if "colours" in fw_comp_model[link0][link1]:
                        fw_comp_model[link0][link1].append(len(date_list)-1)
                    else:
                        fw_comp_model[link0][link1] = {"colours" : [len(date_list)-1]}

plt.figure(figsize=(25,10))



if origin in fw_comp_model:
    for key, values in fw_comp_model[origin].items():
        reference = values["ref"]
        observed = values["obs"]
        colours = ['green'] * len(date_list)
        if "colours" in values:
            for index in values["colours"]:
                colours[index] = 'red'
        if len(values["ref"]) == len(date_list):
            plt.plot(np.arange(len(date_list)), reference, color = 'blue')
            plt.plot(np.arange(len(date_list)), observed, color = colours)
            

#start graphing




#plt.boxplot(rtt_intervallist)
#plt.plot(date_list)
plt.xticks(np.arange(len(date_list)),date_list,rotation='vertical')

#err_list = [rtt_lower, rtt_upper]


#plt.fill_between(np.arange(96), normal_reference_lower, normal_reference_upper, color='b', alpha=.1)

#plt.errorbar(np.arange(96), rtt_median, yerr=err_list, fmt='o',capsize=5)

plt.savefig('results/fw_graph_58.png')

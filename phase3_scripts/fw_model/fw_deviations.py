import ujson 
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import ast 

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

# Date format = 2020-10-20
start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

# Near-end facility which links are going to be printed in the graph
#origin = sys.argv[3] 
#dest = sys.argv[4]

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date

#Calculate the range of days used for the loop
delta = edate - sdate      

date_list = []

fw_comp_model = {}

# Loop through the days considered in the graph
for date in tqdm(range(delta.days + 1)):

    # "Calculate" what day is going to be looped through
    day = sdate + timedelta(days=date)
 
    # For each hour, add to the fw_comp-dictionary the observed values and the expected usage values of each link with the 
    # "origin" as near-end facility
    # Also adding a list of alarms and r and p values to plot them over the observations
    for hour in tqdm(hours):
        if hour == "00":
            date_list.append(str(day))
        else:
            date_list.append(hour)
        file1 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/fw_model_comparison")
        new_model = ujson.load(file1)

        ### {1: {2:[40,50]}, {3:[40,50]}, {5:[40,0]}, {10:[0,40]}} ###
        for source in new_model:
            for dest, value in new_model[source].items():
                if source in fw_comp_model:
                    if dest in fw_comp_model[source]:
                        if len(value) == 2 and value[0] != 0:
                            #fw_comp_model[source][dest]["ref"].append(value[0])
                            fw_comp_model[source][dest].append(value[1])
                        
                        #fw_comp_model[source][dest]["ref"].append(value[0])
                        #if len(value) == 1:
                        #    fw_comp_model[source][dest]["obs"].append(0)
                        #else:
                        #    fw_comp_model[source][dest]["obs"].append(value[1])
                    else:
                        if len(value) == 2 and value[0] != 0:
                            fw_comp_model[source][dest] = [value[1]]
                        #fw_comp_model[source][dest] = {"ref": [value[0]]}
                        #if len(value) == 1:
                        #    fw_comp_model[source][dest]["obs"] = [0]
                        #else:
                        #    fw_comp_model[source][dest]["obs"] = [value[1]]       
                else:
                    if len(value) == 2 and value[0] != 0:
                        fw_comp_model[source] = {dest : [value[1]]}
                    #fw_comp_model[source] = {dest : {"ref": [value[0]]}}
                    #if len(value) == 1:
                    #    fw_comp_model[source][dest]["obs"] = [0]
                    #else:
                    #    fw_comp_model[source][dest]["obs"] = [value[1]]
        file1.close()
        
    


# Creation of the base figure with the size
plt.figure(figsize=(100,10))

link_list = []
dev_list = []

for source in fw_comp_model:
    for dest, values in fw_comp_model[source].items():
        if len(values) == len(date_list):
            dev_list.append(np.std(values))
            link_list.append(str([source, dest]))

plt.scatter(np.arange(len(link_list)), dev_list)

# Set the ticks of the X Axis 
plt.xticks(np.arange(len(link_list)),link_list,rotation='vertical')

plt.legend()

# save the figure in a folder
save_path = "../results/fw_deviations_" + str(sdate) + "_" + str(edate) + "_.png"
plt.savefig(save_path)

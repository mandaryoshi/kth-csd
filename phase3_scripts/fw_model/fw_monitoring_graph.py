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
origin = sys.argv[3] 
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

        file2 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/fw_alarms")
        alarms = ujson.load(file2)
        ### {1: {2:[40,50]}, {3:[40,50]}, {5:[40,0]}, {10:[0,40]}} ###
        for source in new_model:
            for dest, value in new_model[source].items():
                if source in fw_comp_model:
                    if dest in fw_comp_model[source] and dest != "p_value":
                        if len(value["comp"]) == 2 and value["comp"][0] != 0:
                            fw_comp_model[source][dest]["ref"].append(value["comp"][0])
                            fw_comp_model[source][dest]["obs"].append(value["comp"][1])
                            fw_comp_model[source][dest]["probes"].append(len(value["probes"]))
                        #fw_comp_model[source][dest]["ref"].append(value[0])
                        #if len(value) == 1:
                        #    fw_comp_model[source][dest]["obs"].append(0)
                        #else:
                        #    fw_comp_model[source][dest]["obs"].append(value[1])
                    else:
                        print(value)
                        if len(value["comp"]) == 2 and value["comp"][0] != 0:
                            fw_comp_model[source][dest] = {
                                "ref": [value["comp"][0]], 
                                "obs": [value["comp"][1]],
                                "probes": [len(value["probes"])]
                            }
                        #fw_comp_model[source][dest] = {"ref": [value[0]]}
                        #if len(value) == 1:
                        #    fw_comp_model[source][dest]["obs"] = [0]
                        #else:
                        #    fw_comp_model[source][dest]["obs"] = [value[1]]       
                else:
                    print(value["comp"][0])
                    if len(value["comp"]) == 2 and value["comp"][0] != 0:
                        fw_comp_model[source] = {
                            dest : {
                                "ref": [value["comp"][0]], 
                                "obs": [value["comp"][1]],
                                "probes": [len(value["probes"])]
                            }
                        }
                    #fw_comp_model[source] = {dest : {"ref": [value[0]]}}
                    #if len(value) == 1:
                    #    fw_comp_model[source][dest]["obs"] = [0]
                    #else:
                    #    fw_comp_model[source][dest]["obs"] = [value[1]]
        file1.close()
        for key in alarms["alarms"]:
            link0 = key[0]
            link1 = key[1]
            if link0 == origin:
                print("alarm")
            if link0 in fw_comp_model:
                if link1 in fw_comp_model[link0]:
                    if "alarms" in fw_comp_model[link0][link1]:
                        fw_comp_model[link0][link1]["alarms"].append(len(date_list)-1)
                        fw_comp_model[link0][link1]["r_p_value"].append((key[2], key[3]))

                    else:
                        fw_comp_model[link0][link1]["alarms"] =  [len(date_list)-1]
                        fw_comp_model[link0][link1]["r_p_value"] = [(key[2], key[3])]
                    
        file2.close()


# Creation of the base figure with the size
fig, ax = plt.subplots(2, sharex=True, gridspec_kw={'hspace': 0})

# For every link of the origin near-end facility, check if it appears in every hour of the period observed
# and create 3 lists that will be plotted corresponding to the expected values, the observed, and the alarms triggered
if origin in fw_comp_model:
    for dest, values in fw_comp_model[origin].items():
        reference = values["ref"]
        observed = values["obs"]
        probes = values["probes"]
        alarm_values = []
        if len(observed) == len(date_list):
            if "alarms" in values:
                for index in values["alarms"]:
                    alarm_values.append(observed[index])

                #plt.scatter(values["alarms"], alarm_values, color = 'red', label=values["r_p_value"])
                ax[0].scatter(values["alarms"], alarm_values, color = 'red')
            if len(values["ref"]) == len(date_list):
                ax[0].plot(np.arange(len(date_list)), reference, color = 'blue')
                ax[0].plot(np.arange(len(date_list)), observed, label=dest)
                ax[1].plot(np.arange(len(date_list)), probes, label=dest)


# Set the ticks of the X Axis 
#plt.xticks(np.arange(len(date_list)),date_list,rotation='vertical')
ax[1].set_xticks(date_list,rotation='vertical')

plt.legend()

# save the figure in a folder
save_path = "../results/fw_graph_alarms_" + origin + "_probes.png"
plt.savefig(save_path)

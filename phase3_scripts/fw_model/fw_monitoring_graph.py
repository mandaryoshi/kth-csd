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

cities = ujson.load(open("json_results/fac_loc_results.json"))

date_list = []
graph_list = []
counter_list = []


fw_comp_model = {}

# Loop through the days considered in the graph
counter = 0
for date in tqdm(range(delta.days + 1)):

    # "Calculate" what day is going to be looped through
    day = sdate + timedelta(days=date)
 
    # For each hour, add to the fw_comp-dictionary the observed values and the expected usage values of each link with the 
    # "origin" as near-end facility
    # Also adding a list of alarms and r and p values to plot them over the observations
    
    for hour in tqdm(hours):
        if hour == "00":
            if counter % 168 == 0:
                date_list.append(str(day))
                graph_list.append(str(day))
                counter_list.append(counter)
            else:
                date_list.append(None)
        else:
            date_list.append(None)

        counter = counter + 1

        file1 = open("../traceroutes/" + str(day) + "/" + hour + "00/fw_model_comparison")
        new_model = ujson.load(file1)

        ### {1: {2:[40,50]}, {3:[40,50]}, {5:[40,0]}, {10:[0,40]}} ###
        for source in new_model:
            for dest, value in new_model[source].items():
                if dest != "p_value":
                    if source in fw_comp_model:
                        if dest in fw_comp_model[source]:
                            if len(value["comp"]) == 2 and value["comp"][0] != 0 and source == origin:
                                fw_comp_model[source][dest]["ref"].append(value["comp"][0])
                                fw_comp_model[source][dest]["obs"].append(value["comp"][1])
                                fw_comp_model[source][dest]["probes"].append(len(value["probes"]))
                        else:
                            if len(value["comp"]) == 2 and value["comp"][0] != 0 and source == origin:
                                fw_comp_model[source][dest] = {
                                    "ref": [value["comp"][0]], 
                                    "obs": [value["comp"][1]],
                                    "probes": [len(value["probes"])]
                                }      
                    else:
                        if len(value["comp"]) == 2 and value["comp"][0] != 0 and source == origin:
                            fw_comp_model[source] = {
                                dest : {
                                    "ref": [value["comp"][0]], 
                                    "obs": [value["comp"][1]],
                                    "probes": [len(value["probes"])]
                                }
                            }
                    
        file1.close()
        
        try:
            #if date >= 7:
            file2 = open("../traceroutes/" + str(day) + "/" + hour + "00/fw_filtered_alarms")
            alarms = ujson.load(file2)
        
        except FileNotFoundError:
            file2 = open("../traceroutes/" + str(day) + "/" + hour + "00/fw_alarms")
            alarms = ujson.load(file2)
            
        for types in alarms.keys():
            for alarm in alarms[types]:
                link0 = alarm[0]
                link1 = alarm[1]
                if link0 == origin:
                    print("alarm")
                if link0 in fw_comp_model:
                    if link1 in fw_comp_model[link0]:
                        if types in fw_comp_model[link0][link1]:
                            fw_comp_model[link0][link1][types].append(len(date_list)-1)
                            #fw_comp_model[link0][link1]["mse"].append((alarm[4]))

                        else:
                            fw_comp_model[link0][link1][types] =  [len(date_list)-1]
                            #fw_comp_model[link0][link1]["mse"] = [(alarm[4])]

        file2.close()

# # Creation of the base figure with the size
# fig, ax = plt.subplots(2, sharex=True, gridspec_kw={'hspace': 0}, figsize=(30,10))

# ax[0].set_title('Forwarding Pattern for Facility ' + origin)

# ax[0].set_ylabel('# of traceroutes')
# ax[1].set_ylabel('# of unique probes')
# plt.xlabel('Date')


# #ax[1].set_title('Probe Pattern for Facility' + origin)

# # For every link of the origin near-end facility, check if it appears in every hour of the period observed
# # and create 3 lists that will be plotted corresponding to the expected values, the observed, and the alarms triggered
# if origin in fw_comp_model:
#     for dest, values in fw_comp_model[origin].items():
#         if dest != "18":
#             reference = values["ref"]
#             observed = values["obs"]
#             probes = values["probes"]
            
#             if len(observed) == len(date_list):
#                 if "red_alarms" in values:
#                     alarm_values = []
#                     for index in values["red_alarms"]:
#                         alarm_values.append(observed[index])

                
#                     ax[0].scatter(values["red_alarms"], alarm_values, color = 'red')
#                     #for i, txt in enumerate(values["mse"]):
#                         #ax[0].annotate(txt, (values["alarms"][i], alarm_values[i]))
                
#                 if "yellow_alarms" in values:
#                     alarm_values = []
#                     for index in values["yellow_alarms"]:
#                         alarm_values.append(observed[index])

#                     ax[0].scatter(values["yellow_alarms"], alarm_values, color = 'yellow')
                
#                 #ax[0].plot(np.arange(len(date_list)), reference, color = 'blue')
#                 ax[0].plot(np.arange(len(date_list)), observed, label=dest)
#                 ax[1].plot(np.arange(len(date_list)), probes, label=dest)


# # Set the ticks of the X Axis 
# plt.xticks(np.arange(len(date_list)),date_list,rotation='vertical')


# plt.legend()

# # save the figure in a folder
# #save_path = "phase3_scripts/results/fw/fw_graph_" + origin + ".png"
# #plt.savefig(save_path)
# plt.show()


# Creation of the base figure with the size
fig, ax = plt.subplots(1, gridspec_kw={'hspace': 0}, figsize=(9,3))
#9, 3


try:
    ax.set_title('Forwarding Pattern for ' + cities[origin]["name"])
except Exception as e:
    print(e)
    ax.set_title('Forwarding Pattern for Facility ' + origin)

ax.set_ylabel('# of traceroutes')
#plt.xlabel('Date')


#ax[1].set_title('Probe Pattern for Facility' + origin)

# For every link of the origin near-end facility, check if it appears in every hour of the period observed
# and create 3 lists that will be plotted corresponding to the expected values, the observed, and the alarms triggered
if origin in fw_comp_model:
    for dest, values in fw_comp_model[origin].items():
        if dest != "0":
            reference = values["ref"]
            observed = values["obs"]
            probes = values["probes"]
            
            if len(observed) == len(date_list):
                if "red_alarms" in values:
                    alarm_values = []
                    for index in values["red_alarms"]:
                        alarm_values.append(observed[index])
                
                    ax.scatter(values["red_alarms"], alarm_values, edgecolor = 'red', facecolor='None')

                if "yellow_alarms" in values:
                    alarm_values = []
                    for index in values["yellow_alarms"]:
                        alarm_values.append(observed[index])

                    ax.scatter(values["yellow_alarms"], alarm_values, edgecolor = 'orange', facecolor='None')
                
                #ax[0].plot(np.arange(len(date_list)), reference, color = 'blue')
                try:
                    ax.plot(np.arange(len(date_list)), observed, label=cities[dest]["name"])
                except Exception as e:
                    print (e)
                    ax.plot(np.arange(len(date_list)), observed, label=dest)



# Set the ticks of the X Axis 
#plt.xticks(np.arange(len(date_list)),date_list,rotation='5')

print(len(date_list))
print(graph_list)

ax.xaxis.set_major_locator(plt.FixedLocator(counter_list))
ax.set_xticklabels(graph_list, rotation='30', rotation_mode='anchor', horizontalalignment='right')


plt.legend()
plt.grid()
# save the figure in a folder
plt.tight_layout()
#plt.savefig("phase3_scripts/results/fw/fw_graph_" + origin + ".png")
plt.show()
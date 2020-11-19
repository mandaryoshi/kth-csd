import ujson 
import sys
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import ast 
import collections

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

# Date format = 2020-10-20
start_date = sys.argv[1].split('-')
end_date = sys.argv[2].split('-')

# Near-end facility which links are going to be printed in the graph
source = sys.argv[3]
if len(sys.argv) == 5:
    dest_arg = sys.argv[4]
else:
    dest_arg = None

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date

#Calculate the range of days used for the loop
delta = edate - sdate       

date_list = []

fw_dict = {}

# Loop through the days considered in the graph
for date in tqdm(range(delta.days + 1)):
    day = sdate + timedelta(days=date)
    print(date)
    # For each hour, add to the fw dictionary the observed values
    for hour in tqdm(hours):
        if hour == "00":
            date_list.append(str(day))
        else:
            date_list.append(hour)
        file1 = open("/home/csd/traceroutes/" + str(day) + "/" + hour + "00/connections")
        
        connections = ujson.load(file1)

        

        ### {1: {2:[40,50]}, {3:[40,50]}, {5:[40,0]}, {10:[0,40]}} ###
        link_ok = False
        for key in connections:
            link = ast.literal_eval(key)
            #print(val[0])
            #time.sleep(1)
            link0 = str(link[0])
            link1 = str(link[1])

            if source == link0:
                link_ok = True
            
            cnt = collections.Counter(connections[key]["msm_id"])
#            print(cnt)
            if len(connections[key]["rtts"]) > 5 and len(connections[key]["probes"]) > 5:

                if link0 in fw_dict:
                    if link1 in fw_dict[link0]:
                        for msm_id, count in cnt.items():
                            if msm_id in fw_dict[link0][link1]:
                                fw_dict[link0][link1][msm_id].append(count)
                            else:
                                fw_dict[link0][link1][msm_id] = [0]*((date+1)*int(hour)) + [count]
                    else:
                        fw_dict[link0][link1] = None
                        msm_id_dict = {} 
                        for msm_id, count in cnt.items():
                            msm_id_dict[msm_id] = [0]*((date+1)*int(hour)) + [count]
                        fw_dict[link0][link1] = msm_id_dict
                else:
                    #print(link[0])
                    fw_dict[link0] = {link1 : None}
                    msm_id_dict = {}
                    for msm_id, count in cnt.items():
                        msm_id_dict[msm_id] = [0]*((date+1)*int(hour)) + [count]
                    fw_dict[link0][link1] = msm_id_dict
        file1.close()
        # If the near-end facility is not present in all the hours of the observation
        # cancel the plot and print an error message
        if link_ok == False:
            print("INVALID SOURCE")
            sys.exit()
        #print(fw_dict)
        for near in fw_dict:
            for far in fw_dict[near]:
                for msm_id, cnt_list in fw_dict[near][far].items():
                    
                    if len(cnt_list) != len(date_list):
                        fw_dict[near][far][msm_id].append(0)

if dest_arg == None:
    fig, ax = plt.subplots(len(fw_dict[source]), sharex=False, figsize=(80,50))
    index = 0
    for farend in fw_dict[source]:
        title = source + "--->" + farend
        ax[index].set_title(title)
        for msm_id, count in fw_dict[source][farend].items():
        # Only plot the links present in all the hourly time bins
            if len(count) == len(date_list):
                ax[index].plot(np.arange(len(date_list)), count, label=msm_id)
        index = index + 1
else:
    if dest_arg in fw_dict[source]:
        fig, ax = plt.subplots(len(fw_dict[source][dest_arg]), sharex=False, figsize=(300,50))
        index = 0
        for  msm_id, count in fw_dict[source][dest_arg].items():
            ax[index].set_title(msm_id)
            if len(count) == len(date_list):
                ax[index].plot(np.arange(len(date_list)), count)
            index = index + 1
    else:
        print("INVALID SOURCE")
        sys.exit()
#start graphing

#print(fw_dict["58"])


#plt.boxplot(rtt_intervallist)
#plt.plot(date_list)
plt.xticks(np.arange(len(date_list)),date_list,rotation='vertical')

#err_list = [rtt_lower, rtt_upper]


#plt.fill_between(np.arange(96), normal_reference_lower, normal_reference_upper, color='b', alpha=.1)

#plt.errorbar(np.arange(96), rtt_median, yerr=err_list, fmt='o',capsize=5)
if dest_arg == None:
    save_path = "../results/fw_graph_" + source + "_msm.png"
else: 
    save_path = "../results/fw_graph_" + source + "_" + dest_arg +  "_msm.png"
plt.savefig(save_path)

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
source = sys.argv[3]
#dest = sys.argv[4]

sdate = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))   # start date
edate = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))   # end date

#Calculate the range of days used for the loop
delta = edate - sdate       

date_list = []

fw_dict = {}

# Loop through the days considered in the graph
for date in tqdm(range(delta.days + 1)):
    day = sdate + timedelta(days=date)
 
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
            
            if len(connections[key]["rtts"]) > 5 and len(connections[key]["probes"]) > 5:

                if link0 in fw_dict:
                    if link1 in fw_dict[link0]:
                        fw_dict[link0][link1].append(len(connections[key]["rtts"]))
                    else:
                        fw_dict[link0][link1] = [len(connections[key]["rtts"])]
                else:
                    #print(link[0])
                    fw_dict[link0] = {
                        link1 : [len(connections[key]["rtts"])]
                        
                    }
            
        file1.close()
        # If the near-end facility is not present in all the hours of the observation
        # cancel the plot and print an error message
        if link_ok == False:
            print("INVALID SOURCE")
            sys.exit()
            
plt.figure(figsize=(25,10))

for key, count in fw_dict[source].items():
    # Only plot the links present in all the hourly time bins
    if len(count) == len(date_list):
        plt.plot(np.arange(len(date_list)), count)

#start graphing




#plt.boxplot(rtt_intervallist)
#plt.plot(date_list)
plt.xticks(np.arange(len(date_list)),date_list,rotation='vertical')

#err_list = [rtt_lower, rtt_upper]


#plt.fill_between(np.arange(96), normal_reference_lower, normal_reference_upper, color='b', alpha=.1)

#plt.errorbar(np.arange(96), rtt_median, yerr=err_list, fmt='o',capsize=5)

plt.savefig('../results/fw_graph_58.png')

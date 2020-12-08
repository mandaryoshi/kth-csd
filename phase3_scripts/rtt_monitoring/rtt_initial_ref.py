import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import time
from datetime import timedelta, datetime

#Define wilson function to determine confidence interval for differential rtts between two colos in an hour.
def wilson(p, n, z = 1.96):
    denominator = 1 + z**2/n
    centre_adjusted_probability = p + z*z / (2*n)
    adjusted_standard_deviation = sqrt((p*(1 - p) + z*z / (4*n)) / n)
    
    lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator

    return (round(lower_bound*n), round(upper_bound*n))

#Function implementing a sliding window of 24hrs. 
def sliding_window(curr_hour):
     
    hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]
    #n is the number of times "hours" list must be rotated.
    n = hours.index(curr_hour)   
    for i in range(0,n):
        first = hours[0]    
        for j in range(0, len(hours)-1):     
            hours[j] = hours[j+1]    
        hours[len(hours)-1] = first    
    return hours            

curr_date = sys.argv[1] 
curr_hour = sys.argv[2] #hh
#ref_split determines how to split 24 hrs into two splits, and has a value equal to size of the first split
#For example, if 24 hrs is to be split as 18hrs and 6hrs, ref_split needs to be given a value of 18. 
ref_split = sys.argv[3] 

curr_date_dateTime = datetime.strptime(curr_date, "%Y-%m-%d")
previous_date = str((curr_date_dateTime - timedelta(days = 1)).date())

hours = sliding_window(curr_hour)
#To determine if the sliding window has hours from two different days, positions of "00" and "23" in hours is computed
first_hour_index = hours.index("00") #find the index of "00" in hours
last_hour_index = hours.index("23") #find the index of "23" in hours
diff = last_hour_index - first_hour_index

#Check if the hour is in the previous date array or current date array
previous_array =[]
curr_array = []

if diff == -1:
    for i in range(0,(last_hour_index)+1):
        previous_array.append(hours[i])
    for j in range(first_hour_index, len(hours)):
        curr_array.append(hours[j])    
else:
    for i in range(0,len(hours)):
        previous_array.append(hours[i])

hour  = hours[0]   #First hour in hour list
path = "/home/csd/traceroutes/" + previous_date + "/" + hour + "00" + "/connections"
output_file = open("../results/rtt_sw_ref_values",'w')
file = open(path)
links = ujson.load(file)
link_dict = dict.fromkeys(links.keys()) 

for i in hours:  # for each hour 
    deletions_list = []
    hour = i
    if hour in previous_array:
        path = "/home/csd/traceroutes/" + previous_date + "/" + hour + "00" + "/connections"
    elif hour in curr_array:
        #path = "/home/csd/traceroutes/" + str(curr_date_dateTime.date()) + "/" + hour + "00" + "/connections"
        path = "/home/csd/traceroutes/" + str(curr_date_dateTime.date()) + "/" + hour + "00" + "/connections"

    if hour != hours[0]:
        file = open(path)
        links = ujson.load(file)
    
    for link in link_dict.keys():
        if link in links and len(links[link]["rtts"]) > 5:
            sorted_rtts = sorted(links[link]["rtts"])
            normal_ref = np.median(sorted_rtts)
            ranks = wilson(0.5,len(sorted_rtts))
            #print(ranks, len(sorted_rtts))
            interval = (sorted_rtts[ranks[0]], sorted_rtts[ranks[1]])
            print("LINK IS:", link)
            print("LINKS is", links)
            print(link_dict[link])
            if link_dict[link] == None:
                link_dict[link] = {
                    "lower_bd":[interval[0]],
                    "median":[normal_ref],
                    "upper_bd":[interval[1]]
                }
            else:
                link_dict[link]["lower_bd"].append(interval[0])
                link_dict[link]["median"].append(normal_ref)
                link_dict[link]["upper_bd"].append(interval[1])
        else:
            deletions_list.append(link)

    for x in deletions_list:
        del link_dict[x]
    #print(link_dict[link]["actual_rtts"])    
    #print(link_dict)
    file.close()



initial_ref_values = dict.fromkeys(link_dict.keys())
for key, val in link_dict.items():
    lb_array = link_dict[key]["lower_bd"]
    ub_array = link_dict[key]["upper_bd"]
    median_array = link_dict[key]["median"]
    if(int(ref_split) != 24):
        lb_array_1, lb_array_2 = np.split(link_dict[key]["lower_bd"], [int(ref_split)])
        median_array_1, median_array_2 = np.split(link_dict[key]["median"], [int(ref_split)])
        ub_array_1, ub_array_2 = np.split(link_dict[key]["upper_bd"], [int(ref_split)])
        initial_ref_values[key] = {
                "lower_bd" : round((np.median(lb_array_1)*0.1 + np.median(lb_array_2)*0.9),5),                  #giving more weightage to the last hour
                "median" : round((np.median(median_array_1)*0.1 + np.median(median_array_2)*0.9),5),
                "upper_bd" : round((np.median(ub_array_1)*0.1 + np.median(ub_array_2)*0.9),5),
                "diff"     : round(np.median(ub_array) - np.median(lb_array), 5)
        }
    else:
        initial_ref_values[key] = {
                "lower_bd" : round((np.median(lb_array)),5),
                "median" : round((np.median(median_array)),5),
                "upper_bd" : round((np.median(ub_array)),5),
                "diff"     : round(np.median(ub_array) - np.median(lb_array), 5)
        }


output_file.write(ujson.dumps(initial_ref_values))
output_file.close()


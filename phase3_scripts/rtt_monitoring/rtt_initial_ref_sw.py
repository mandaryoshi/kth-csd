#This script is run to compute initial reference by using sliding window method and 1ms threshold
import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import time
from datetime import timedelta, datetime

#Define wilson function to determine confidence interval
def wilson(p, n, z = 1.96):
    denominator = 1 + z**2/n
    centre_adjusted_probability = p + z*z / (2*n)
    adjusted_standard_deviation = sqrt((p*(1 - p) + z*z / (4*n)) / n)
    
    lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator

    return (round(lower_bound*n), round(upper_bound*n))

##########################Sliding Window Method#########################
#Define a function to use 24 hours sliding window reference 
def sliding_window(curr_hour):
    hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]
    
    #n = no of time the array must be rotated. i.e. the current hour = 0100, take 24 hours before as reference
    n = hours.index(curr_hour)   
    for i in range(0,n):
        first = hours[0]    
        for j in range(0, len(hours)-1):     
            hours[j] = hours[j+1]    
        hours[len(hours)-1] = first    
    return hours            

#Retrieve a whole day data as reference computation
curr_date = sys.argv[1] # current date
curr_hour = sys.argv[2] #%hh -- current hour
ref_split = sys.argv[3] # reference splitting for weightage allocation : i.e. [18 hours,6 hours]

#Change input to date format
curr_date_dateTime = datetime.strptime(curr_date, "%Y-%m-%d")
previous_date = str((curr_date_dateTime - timedelta(days = 1)).date())

#Find the past 24 hours refrence for this current hour
hours = sliding_window(curr_hour)

#find the index of "00" in hours 
first_hour_index = hours.index("00")
last_hour_index = hours.index("23")
diff = last_hour_index - first_hour_index

#Check if the hour is in the previous date array or current date array
previous_array =[]
curr_array = []

#Check if the difference between index "23" and index "00" is negative to identify they are in the same day or different
if diff == -1:
    for i in range(0,(last_hour_index)+1):
        previous_array.append(hours[i])
    for j in range(first_hour_index, len(hours)):
        curr_array.append(hours[j])    
else:
    for i in range(0,len(hours)):
        previous_array.append(hours[i])

#Initialize hour
hour  = hours[0]

#Open a json file contains a dictionary of differential rtt between two links
path = "/home/csd/traceroutes/" + previous_date + "/" + hour + "00" + "/connections"

#Create a variable to save the normal reference
output_file = open("../results/rtt_sw_ref_values",'w')

#Open the variable path and load the json file
file = open(path)
links = ujson.load(file)
link_dict = dict.fromkeys(links.keys()) 

#Compute normal reference
for i in hours:
    deletions_list = []
    hour = i
    #Identify the hour location either in previous date or current date
    if hour in previous_array:
        path = "/home/csd/traceroutes/" + previous_date + "/" + hour + "00" + "/connections"
    elif hour in curr_array:
        path = "/home/csd/traceroutes/" + str(curr_date_dateTime.date()) + "/" + hour + "00" + "/connections" 
    #print(path)

    #Open the path based on hour location and load the json file
    if hour != hours[0]:
        file = open(path)
        links = ujson.load(file)
    
    #Compute normal reference
    for link in link_dict.keys():
        #Only consider the link that consists of more than 5 traceroutes
        if link in links and len(links[link]["rtts"]) > 5:
            #Sort the rtt list for each link, compute the median and the wilson scores
            sorted_rtts = sorted(links[link]["rtts"])
            normal_ref = np.median(sorted_rtts)
            ranks = wilson(0.5,len(sorted_rtts))
            #print(ranks, len(sorted_rtts))

            #Define a confidence interval based on Wilson scores for each link (lower_bound, upper_bound)
            interval = (sorted_rtts[ranks[0]], sorted_rtts[ranks[1]])

            #Create a dictionary that consists of three items below
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
            #For unstable links are collected in an array and then discarded
            deletions_list.append(link)

    for x in deletions_list:
        del link_dict[x]
    file.close()

#Using sliding window with reference splitting method
#Open "link_dict" dictionary which for each link consists of 3 items with 1 item consists of 24 values 
initial_ref_values = dict.fromkeys(link_dict.keys())
for key, val in link_dict.items():
    #Split 1 item into two with the number of values depend of given ref_split (i.e. 18 and 6)
    lb_array_1, lb_array_2 = np.split(link_dict[key]["lower_bd"], [int(ref_split)])
    median_array_1, median_array_2 = np.split(link_dict[key]["median"], [int(ref_split)])
    ub_array_1, ub_array_2 = np.split(link_dict[key]["upper_bd"], [int(ref_split)])
    #Recompute the normal reference items by giving more weightage to the last group of hours
    initial_ref_values[key] = {
        "lower_bd" : round((np.median(lb_array_1)*0.1 + np.median(lb_array_2)*0.9),5),
        "median" : round((np.median(median_array_1)*0.1 + np.median(median_array_2)*0.9),5),
        "upper_bd" : round((np.median(ub_array_1)*0.1 + np.median(ub_array_2)*0.9),5)
    }

#Dump the new dictionary to a json file
output_file.write(ujson.dumps(initial_ref_values))
output_file.close()


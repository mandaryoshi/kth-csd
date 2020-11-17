import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import scipy.stats as st
import time

#Define wilson function to determine confidence interval
def wilson(p, n, z = 1.96):
    denominator = 1 + z**2/n
    centre_adjusted_probability = p + z*z / (2*n)
    adjusted_standard_deviation = sqrt((p*(1 - p) + z*z / (4*n)) / n)
    
    lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator

    return (round(lower_bound*n), round(upper_bound*n))

#Retrieve a whole day data as reference computation
date = sys.argv[1]
hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]
hour  = hours[0]
path = "/home/csd/traceroutes/" + date + "/" + hour + "00" + "/connections"
output_file = open("../results/rtt_ref_values",'w')
file = open(path)
links = ujson.load(file)
link_dict = dict.fromkeys(links.keys()) 
#print(link_dict)
for i in hours:
    deletions_list = []
    hour = i
    if hour !=  "00":
        file = open("/home/csd/traceroutes/" + date + "/" + hour + "00" + "/connections")
        links = ujson.load(file)
    for link in tqdm(link_dict.keys()):
        if link in links and len(links[link]["rtts"]) > 5:
            sorted_rtts = sorted(links[link]["rtts"])
            normal_ref = np.median(sorted_rtts)
            ranks = wilson(0.5,len(sorted_rtts))
            #print(ranks, len(sorted_rtts))
            interval = (sorted_rtts[ranks[0]], sorted_rtts[ranks[1]])
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
            #print("Wilson confidence interval", interval)
            #print(normal_ref)
            #print("python confidence intervals", st.norm.interval(alpha=0.95, loc=normal_ref, scale=st.sem(sorted_links1)))
            #time.sleep(1)
        else:
            deletions_list.append(link)
    #print(deletions_list)
    for x in deletions_list:
        del link_dict[x]
    file.close()

print(hour)

initial_ref_values = dict.fromkeys(link_dict.keys())
for key, val in link_dict.items():
    initial_ref_values[key] = {
        "lower_bd" : round(np.median(link_dict[key]["lower_bd"]),5),
        "median" : round(np.median(link_dict[key]["median"]),5),
        "upper_bd" : round(np.median(link_dict[key]["upper_bd"]),5)
    }
output_file.write(ujson.dumps(initial_ref_values))
output_file.close()

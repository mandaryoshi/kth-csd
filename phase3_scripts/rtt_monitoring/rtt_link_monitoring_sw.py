#This script is run to identify the alarm based on the difference between the current interval and 
#initial reference interval
import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import time
from shutil import copyfile

#Define wilson function to determine confidence interval
def wilson(p, n, z = 1.96):
    denominator = 1 + z**2/n
    centre_adjusted_probability = p + z*z / (2*n)
    adjusted_standard_deviation = sqrt((p*(1 - p) + z*z / (4*n)) / n)

    lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator

    return (round(lower_bound*n), round(upper_bound*n))


#Give the current date and hour for link monitoring
date = sys.argv[1]
hour = sys.argv[2] 

#path for fetching the hourly connection values
connections_path = "/home/csd/traceroutes/" + date + "/" + hour + "/connections"
file = open(connections_path)
links = ujson.load(file)

#path for fetching the reference values
ref_file = open("../results/rtt_sw_ref_values")
ref = ujson.load(ref_file)

#path to save the old reference values in the beginning
save_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_ref_values"
ref_path = "../results/rtt_sw_ref_values"
copyfile(ref_path, save_path)

median_dict = {}
alarm_dict = {"alarms" : []}

#Compute the current vaues
for link in ref.keys():
    #Only consider the link that consists of more than 5 traceroutes
    if link in links and len(links[link]["rtts"]) > 5:
        #Sort the rtt list for each link, compute the median and the wilson scores
        sorted_rtts = sorted(links[link]["rtts"])
        normal_ref = np.median(sorted_rtts)
        ranks = wilson(0.5,len(sorted_rtts))
        #print(ranks, len(sorted_rtts))

        #Define a confidence interval based on Wilson scores for each link (lower_bound, upper_bound)
        interval = (round(sorted_rtts[ranks[0]],5), round(sorted_rtts[ranks[1]],5))

        #Fetch reference interval from initial reference computation
        ref_interval = (ref[link]["lower_bd"],ref[link]["upper_bd"])

        #To detect the alarm, examine the difference between current interval and initial reference interval
        #Use 1 ms as the threshold for difference
        if (((interval[0] - ref_interval[1]) > 1) or  ((ref_interval[0] - interval[1]) > 1)):
            #print("Alarm triggered!!", link, interval, ref_interval)
            alarm_dict["alarms"].append(link)

        #Append the three items below to new dictionary as the current value (lower_bound, median, and upper_bound)
        median_dict[link] = {
            "lower_bd" : interval[0],
            "median" : normal_ref,
            "upper_bd" : interval[1]
        }

ref_file.close()

#Dump the current dictionary to a json file
results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_medians"
with open(results_path, 'w') as fp:
    ujson.dump(median_dict, fp)

fp.close()

#Dump alarm dictionary to a json file
results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_alarms"
with open(results_path, 'w') as fp:
    ujson.dump(alarm_dict, fp)

fp.close()

print(date, hour)

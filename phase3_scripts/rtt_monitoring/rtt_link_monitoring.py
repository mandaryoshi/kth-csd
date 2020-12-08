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
actual_rtt_dict = {}

for link in ref.keys():
    if link in links and len(links[link]["rtts"]) > 5:
        sorted_rtts = sorted(links[link]["rtts"])
        normal_ref = np.median(sorted_rtts)
        index = np.argsort(links[link]["rtts"])[len(links[link]["rtts"])//2]
        #index = np.argsort(sorted_rtts)[len(sorted_rtts)//2]
        #print("Index", index)
        ranks = wilson(0.5,len(sorted_rtts))
        #print(ranks, len(sorted_rtts))
        interval = (round(sorted_rtts[ranks[0]],5), round(sorted_rtts[ranks[1]],5))
        ref_interval = (ref[link]["lower_bd"],ref[link]["upper_bd"])
        if (((interval[0] - ref_interval[1]) > ref[link]["diff"]) or  ((ref_interval[0] - interval[1]) > ref[link]["diff"])):
            actual_rtt = links[link]["actual_rtts"][index]
            #print(actual_rtt)
            alarm_dict["alarms"].append(link)
            actual_rtt_dict[link] = (round(actual_rtt[0],5), round(actual_rtt[1],5), ref[link]["diff"])

#print("Seba:", actual_rtt_dict)
ref_file.close()
results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_medians"
with open(results_path, 'w') as fp:
    ujson.dump(median_dict, fp)

fp.close()

results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_alarms"
with open(results_path, 'w') as fp:
    ujson.dump(alarm_dict, fp)

fp.close()

results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/actual_rtt_sw_alarms"
with open(results_path, 'w') as fp:
    ujson.dump(actual_rtt_dict, fp)

fp.close()


print(date, hour)

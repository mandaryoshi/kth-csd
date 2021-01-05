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
        ranks = wilson(0.5,len(sorted_rtts))
        interval = (round(sorted_rtts[ranks[0]],5), round(sorted_rtts[ranks[1]],5))
        ref_interval = (ref[link]["lower_bd"],ref[link]["upper_bd"])
        # An alarm is raised if the gap between confidence interval measured for the current hour and the reference 
        # confidence interval hour is more than a threshold value. This threshold value is different for different facility pairs.
        if (((interval[0] - ref_interval[1]) > ref[link]["diff"]) or  ((ref_interval[0] - interval[1]) > ref[link]["diff"])):
            actual_rtt = links[link]["actual_rtts"][index]
            alarm_dict["alarms"].append(link)
            actual_rtt_dict[link] = (round(actual_rtt[0],5), round(actual_rtt[1],5), ref[link]["diff"])
        # Write the median rtt values and lower and upper bounds of confidence intervals for a link to a dictionary.
        median_dict[link] = {
		"lower_bd": interval[0], 
		"median": normal_ref,
		"upper_bd": interval[1]
        }

ref_file.close()
# Store the rtt values including the median and lower bound and upper bound for the confidence interval for the current measured hour.
results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_medians"
with open(results_path, 'w') as fp:
    ujson.dump(median_dict, fp)
fp.close()

# Store the alarms raised for the current measured hour.
results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_sw_alarms"
with open(results_path, 'w') as fp:
    ujson.dump(alarm_dict, fp)
fp.close()

# Store the actual rtt values for alarm cases.
results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/actual_rtt_sw_alarms"
with open(results_path, 'w') as fp:
    ujson.dump(actual_rtt_dict, fp)
fp.close()

print(hour)
print('Number of alarms raised:', len(alarm_dict['alarms']))
if (len(alarm_dict['alarms']) != 0):
    print('Anomalous RTT pattern observed at links:', alarm_dict['alarms'])

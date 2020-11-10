import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import scipy.stats as st
import time
from shutil import copyfile

a = 0.03

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
ref_file = open("results/rtt_ref_values")
ref = ujson.load(ref_file)

#path to save the old reference values in the beginning
save_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_ref_values"
ref_path = "results/rtt_ref_values"
copyfile(ref_path, save_path)

median_dict = {}
alarm_dict = {"alarms" : []}

for link in ref.keys():
    if link in links and len(links[link]) > 5:
        sorted_rtts = sorted(links[link])
        normal_ref = np.median(sorted_rtts)
        ranks = wilson(0.5,len(sorted_rtts))
        #print(ranks, len(sorted_rtts))
        interval = (round(sorted_rtts[ranks[0]],5), round(sorted_rtts[ranks[1]],5))
        ref_interval = (ref[link]["lower_bd"],ref[link]["upper_bd"])
        if (((interval[0] - ref_interval[1]) > 1) or  ((ref_interval[0] - interval[1]) > 1)):
            print("Alarm triggered!!", link, interval, ref_interval)
            alarm_dict["alarms"].append(link)

        median_dict[link] = {
            "lower_bd" : interval[0],
            "median" : normal_ref,
            "upper_bd" : interval[1]
        }

        ref[link] = {
            "lower_bd" : round(interval[0]*a + ref_interval[0]*(1-a),5),
            "median" : round(normal_ref*a  + (ref[link]["median"])*(1-a),5),
            "upper_bd" : round(interval[1]*a + ref_interval[1]*(1-a),5)
	    }

ref_file.close()
ref_file = open("results/rtt_ref_values", 'w')
ref_file.write(ujson.dumps(ref))
ref_file.close()

results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_medians"
with open(results_path, 'w') as fp:
    ujson.dump(median_dict, fp)

fp.close()

results_path = "/home/csd/traceroutes/" + date + "/" + hour + "/rtt_alarms"
with open(results_path, 'w') as fp:
    ujson.dump(alarm_dict, fp)

fp.close()
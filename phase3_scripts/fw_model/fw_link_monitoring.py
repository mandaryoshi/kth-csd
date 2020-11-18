import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
from scipy.stats import chisquare
import time
import ast

# Input the date and hour for forwarding model link monitoring
# Date format = 2020-10-20
# Hour format = 18
date = sys.argv[1]
hour = sys.argv[2]

# Path for the hour you are monitoring
path = "/home/csd/traceroutes/" + date + "/" + hour + "00/connections"
file = open(path)
links = ujson.load(file)

# Path for the reference values, for now, the past 3 hours
ref_path = "/home/csd/traceroutes/" + date + "/" + hour + "00/fw_references"
ref_file = open(ref_path)
ref = ujson.load(ref_file)

# Function to calculate the responsibility metric
# Given one list of values (observed and reference)
# Return the r value for each link in a dictionary format
def r_values(src_fw_dict):
    r_values_dict = {}
    denom = 0
    for val in src_fw_dict.values():
        if len(val) > 1:
            denom = denom + abs(val[1] - val[0])
        else:
            denom = denom + abs(0 - val[0])

    for dest, value in src_fw_dict.items():
        if len(value) > 1:
            num = (value[1] - value[0])
        else:
             num = (0 - value[0])

        try:
            r_values_dict[dest] = round(num/denom,2)
        except ZeroDivisionError: 
            r_values_dict[dest] = round(0,2)
    return r_values_dict

# Create a new forwarding dictionary for the new values starting off
# with the fw_reference values from the previous 3 hours
# Format example of the dictionary:
# {Fac1: {Fac2:[40]}, {Fac3:[45]}, {Fac5:[40]}, {Fac10:[60]}}

fw_dict = ref

# For each link used in this hour, append the usage value to the ref list for comparison,
# if the link is not in the dictionary, a new entry is created with ref value 0
for key in links:
    
    link = ast.literal_eval(key)
    link0 = str(link[0])
    link1 = str(link[1])

    if link0 in fw_dict and len(links[key]["rtts"]) > 5 and len(links[key]["probes"]) > 4:
        if link1 in fw_dict[link0]:
            fw_dict[link0][link1] = { 
                "comp":  [fw_dict[link0][link1][0], len(links[key]["rtts"])],
                "probes": links[key]["probes"]
            }
            #fw_dict[link0][link1]["comp"].append(len(links[key]["rtts"]))
            #fw_dict[link0][link1]["probes"].append(links[key]["probes"])
        else:
            fw_dict[link0][link1] = { 
                "comp":  [0,len(links[key]["rtts"])],
                "probes": links[key]["probes"]
            }
 

# Creating a dictionary to store the alarms
alarm_dict = {"alarms" : []}

# Two lists to compare with the chisquare test: the reference list and the observed list
for source in fw_dict.keys():
    ref_list = []
    results_list = []
    for dest, val in fw_dict[source].items():
        #ref_list.append(val[0])
        #dests.append(dest)
        #if len(val) == 1:
            #results_list.append(0)
        if val["comp"][0] != 0 and len(val["comp"]) == 2:        # only compare the links that have a reference value and 
            ref_list.append(val["comp"][0])              # an observation different than 0
            results_list.append(val["comp"][1])          # This way we ensure the continuity of the data
        #else:
            #results_list.append(val[1])
    #print(ref_list, results_list)
    # First compute the chi squared test
    # Then, if the chi sqaure result detects an anomaly, check the link using the responsibility metric
    if len(ref_list) > 0 and len(results_list) > 0:
        p_value = chisquare(ref_list, results_list)[1]
        fw_dict[source]["p_value"] = p_value
        if p_value <= 0.01:
            r_val_dict = r_values(fw_dict[source])
            for dest in r_val_dict:
                if r_val_dict[dest] < -0.5 or r_val_dict[dest] > 0.5:
                    alarm_dict["alarms"].append((source, dest, r_val_dict[dest], p_value))
    #else:
        #print("empty ref and results list")

print(len(alarm_dict["alarms"]))

# Save alarms and references
output_path = "/home/csd/traceroutes/" + date + "/" + hour + "00/fw_alarms"
output_file = open(output_path,'w')
output_file.write(ujson.dumps(alarm_dict))
output_file.close()

comparison_out_path = "/home/csd/traceroutes/" + date + "/" + hour + "00/fw_model_comparison"
comparison_out_file = open(comparison_out_path,'w')
comparison_out_file.write(ujson.dumps(fw_dict))
comparison_out_file.close()

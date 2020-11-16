import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
from scipy.stats import chisquare
import time
import ast

np.seterr(divide='ignore', invalid='ignore')

date = sys.argv[1]
hour = sys.argv[2]

path = "/home/csd/traceroutes/" + date + "/" + hour + "00/connections"
file = open(path)
links = ujson.load(file)

#change the path
ref_path = "/home/csd/traceroutes/" + date + "/" + hour + "00/fw_references"
ref_file = open(ref_path)
ref = ujson.load(ref_file)

#path to save the old reference values in the beginning
#save_path = "/home/csd/traceroutes/" + date + "/" + hour + "/fw_ref_values"
#ref_path = "results/fw_ref_values"
#copyfile(ref_path, save_path)

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

#create a new forwarding dictionary for the new values
fw_dict = ref

### {1: {2:[40,50]}, {3:[40,50]}, {5:[40,0]}, {10:[0,40]}} ###

for key in links:
    
    link = ast.literal_eval(key)
    link0 = str(link[0])
    link1 = str(link[1])

    if link0 in fw_dict and len(links[key]) > 5:
        if link1 in fw_dict[link0]:
            fw_dict[link0][link1].append(len(links[str(link)]))
        else:
            fw_dict[link0][link1] = [0,len(links[str(link)])]
 

alarm_dict = {"alarms" : []}

#two lists to compare
for source in fw_dict.keys():
    dests = []
    ref_list = []
    results_list = []
    for dest, val in fw_dict[source].items():
        ref_list.append(val[0])
        dests.append(dest)
        if len(val) == 1:
            results_list.append(0)
        else:
            results_list.append(val[1])
    #first compute the chi sqaured test
    p_value = chisquare(results_list, ref_list)[1]
    if p_value > 0.01:
        r_val_dict = r_values(fw_dict[source])
        for dest in r_val_dict:
            if r_val_dict[dest] < -0.25:
                alarm_dict["alarms"].append((source, dest, r_val_dict[dest]))

#save alarms and references

print(len(alarm_dict["alarms"]))

output_path = "/home/csd/traceroutes/" + date + "/" + hour + "00/fw_alarms"
output_file = open(output_path,'w')
output_file.write(ujson.dumps(alarm_dict))
output_file.close()

comparison_out_path = "/home/csd/traceroutes/" + date + "/" + hour + "00/fw_model_comparison"
comparison_out_file = open(comparison_out_path,'w')
comparison_out_file.write(ujson.dumps(fw_dict))
comparison_out_file.close()

#then, if the chi sqaure result detects an anomaly, check the link using the responsibility metric
"""
for src in fw_dict.keys():    
    
    denom = 0
    for val in fw_dict[src].values():
        if len(val) > 1:
            denom = denom + abs(val[1] - val[0])
        else:
            denom = denom + abs(0 - val[0])

    for dest, value in fw_dict[src].items():
        if len(value) > 1:
            num = (value[1] - value[0])
        else:
             num = (0 - value[0])

        try:
            fw_dict[src][dest] = round(num/denom,2)
        except ZeroDivisionError: 
            fw_dict[src][dest] = round(0,2)
print(fw_dict) 
"""


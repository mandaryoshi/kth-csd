import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import time
import ast
import datetime as dt

#sys.path.insert(0, '/mnt/d/Documents/IK2200HT201-IXP')

#Input the date and hour we are analysing
# Date format = 2020-10-20
# Hour format = 18
date = sys.argv[1]
hour = sys.argv[2]

split_date = date.split('-')
sdate = dt.date(int(split_date[0]), int(split_date[1]), int(split_date[2]))   

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

# List of indices that will be taken into account to calculate the forwarding model medians
index_interval = []

interval_length = 9

for value in np.arange(interval_length):
    index_interval.append((int(hour) - value - 1) % 24)

index_interval.reverse()     

fw_dict = {}

#Looping through the past 3 hours to calculate the reference values
for h in index_interval:

    if index_interval[0] >= (24 - interval_length) and h not in np.arange(interval_length):
        day = sdate + dt.timedelta(days= -1)
        path = "/home/csd/traceroutes/" + str(day) + "/" + hours[h] + "00" + "/connections"
    else:
        path = "/home/csd/traceroutes/" + date + "/" + hours[h] + "00" + "/connections"

    file = open(path)
    links = ujson.load(file)
    
    # Looping through the links of an hour to create a dictionary that contains the 
    # lists for each link and the values for all the hours accounting for the median.
    # Format example of the dictionary:
    # {Fac1: {Fac2:[40,50,30]}, {Fac3:[40,50,45]}, {Fac5:[40,30,50]}, {Fac10:[60,40,50]}}

    for key in links:

        link = ast.literal_eval(key)

        link0 = str(link[0])
        link1 = str(link[1])

        if len(links[key]["rtts"]) > 5 and len(links[key]["probes"]) > 4:
            if link0 in fw_dict:
                if link1 in fw_dict[link0]:
                    fw_dict[link0][link1]["comp"].append(len(links[key]["rtts"]))
                else:
                    fw_dict[link0][link1] = {
                        "comp": [len(links[key]["rtts"])]
                    }
            else:
                fw_dict[link0] = {
                    link1 :{ 
                       "comp": [len(links[key]["rtts"])]
                    }
                }

    file.close()

# Substituting the lists of values for the median references
# Format example of the dictionary:
# {Fac1: {Fac2:[40]}, {Fac3:[45]}, {Fac5:[40]}, {Fac10:[50]}}
# Delete links that are not present in all the hours 

for key in list(fw_dict.keys()):
    for dest, value in list(fw_dict[key].items()):
        if len(fw_dict[key][dest]["comp"]) == len(index_interval):
            index = len(value["comp"])//2
            #fw_dict[key][dest]["comp"] = [0.9*np.median(value["comp"][index:]) + 0.1*np.median(value["comp"][:index])]
            fw_dict[key][dest]["comp"] = [np.median(value["comp"])]
        else: 
            del fw_dict[key][dest]

# Save the forwarding values in the respective folder for the date and hour
output_path = "/home/csd/traceroutes/" + date + "/" + hour + "00/fw_references"
output_file = open(output_path,'w')
output_file.write(ujson.dumps(fw_dict))
output_file.close()


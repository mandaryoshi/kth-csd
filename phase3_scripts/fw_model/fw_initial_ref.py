import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
#import scipy.stats as st
import time
import ast
#from datetime import date, timedelta
import datetime as dt

date = sys.argv[1]
hour = sys.argv[2]

split_date = date.split('-')

sdate = dt.date(int(split_date[0]), int(split_date[1]), int(split_date[2]))   # start date
#delta = sdate
#range(delta.days - 1)

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

index_interval = ((int(hour)-3)%24,(int(hour)-2)%24,(int(hour)-1)%24)

fw_dict = {}

for h in index_interval:

    if index_interval[0] >= 21 and h not in [0,1,2]:
        day = sdate + dt.timedelta(days= -1)
        path = "/home/csd/traceroutes/" + str(day) + "/" + hours[h] + "00" + "/connections"
    else:
        path = "/home/csd/traceroutes/" + date + "/" + hours[h] + "00" + "/connections"
    #print(path)
    file = open(path)
    links = ujson.load(file)

    for key in links:

        link = ast.literal_eval(key)

        link0 = str(link[0])
        link1 = str(link[1])

        if len(links[key]["rtts"]) > 5 and len(links[key]["probes"] > 4):
            if link0 in fw_dict:
                if link1 in fw_dict[link0]:
                    fw_dict[link0][link1].append(len(links[key]["rtts"]))
                else:
                    fw_dict[link0][link1] = [len(links[key]["rtts"])]
            else:
                fw_dict[link0] = {
                    link1 : [len(links[key]["rtts"])]
                }

    file.close()

for key in fw_dict.keys():
    for dest, value in fw_dict[key].items():
        fw_dict[key][dest] = [np.median(value)]

output_path = "/home/csd/traceroutes/" + date + "/" + hour + "00/fw_references"
output_file = open(output_path,'w')
output_file.write(ujson.dumps(fw_dict))
output_file.close()


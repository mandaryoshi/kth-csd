import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import scipy.stats as st
import time
import ast

hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
         "14","15","16","17","18","19","20","21","22","23"]

output_file = open("results/fw_ref_values",'w')


input_file = open("results/rtt_ref_values",'r')
rtt_ref_values = ujson.load(input_file)


link_list = list(rtt_ref_values.keys()) 
fw_dict = {}
for hour in hours:
    path = "/home/csd/traceroutes/" + "2020-11-01" + "/" + hour + "00" + "/connections"
    file = open(path)
    links = ujson.load(file)

    for link in tqdm(link_list):
        link = ast.literal_eval(link)
        #print(val[0])
        #time.sleep(1)

        link[0] = str(link[0])
        link[1] = str(link[1])

        if link[0] in fw_dict:
            if link[1] in fw_dict[link[0]]:
                fw_dict[link[0]][link[1]].append(len(links[str(link)]))
            else:
                fw_dict[link[0]][link[1]] = [len(links[str(link)])]
        else:
            #print(link[0])
            fw_dict[link[0]] = {
                link[1] : [len(links[str(link)])]
            }


    file.close()

for key in fw_dict.keys():
    for dest, value in fw_dict[key].items():
        fw_dict[key][dest] = [np.median(value)]


output_file.write(ujson.dumps(fw_dict))
output_file.close()

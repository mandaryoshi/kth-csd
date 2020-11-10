import ujson 
import sys
from tqdm import tqdm
import numpy as np
from math import sqrt
import scipy.stats as st
import time
import ast


a = 0.03

date = sys.argv[1]
hour = sys.argv[2]

path = "/home/csd/traceroutes/" + date + "/" + hour + "/connections"
file = open(path)
links = ujson.load(file)

ref_file = open("results/fw_ref_values")
ref = ujson.load(ref_file)

#create a new forwarding dictionary for the new values
fw_dict = ref

### {1: {2:[40,50]}, {3:[40,50]}, {5:[40,0]}, {10:[0,40]}} ###

for link in tqdm(links):
    link = ast.literal_eval(link)
    if link[0] in fw_dict:
        if link[1] in fw_dict[link[0]]:
            fw_dict[link[0]][link[1]].append(len(links[str(link)]))
        else:
            fw_dict[link[0]][link[1]] = [0,len(links[str(link)])]


#compare the two forwarding dictionaries
for src in fw_dict.keys():    
    
    denom = 0
    for val in src.values():
        if len(val) > 1:
            denom = denom + abs(val[1] - val[0])
        else:
            denom = denom + abs(0 - val[0])

    for dest, value in src.items():
        if len(value) > 1:
            num = (value[1] - value[0])
        else:
             num = (0 - value[0])
        fw_dict[src][value] = round(num/denom,2)

print(fw_dict) 


#ref_file = open("results/fw_ref_values", 'w')
#ref_file.write(ujson.dumps(ref))
#ref_file.close()

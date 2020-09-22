#!/usr/bin/python
import json
import ijson
from tqdm import tqdm
import time





#with open('../traceroute-2020-09-14T1100') as readfile:
#    json_data = ijson.items(readfile, '')

json_data=[]
id = 0
traceroute_dict = {}
with open('../traceroute-2020-09-14T1100','r') as readfile:

    for line in readfile:
        print(line)
        time.sleep(1)
        
        for dataset in line:
            print('\n')
            #print(dataset)
            #print(line[1])
    
#!/usr/bin/python
import json
from tqdm import tqdm
import time





#with open('../traceroute-2020-09-14T1100') as readfile:
#    json_data = ijson.items(readfile, '')

json_data=[]
id = 0
traceroute_dict = {}
with open('example_traceroute','r') as readfile:

    for line in readfile:
        json_line = json.loads(line)
        #for dataset in json_line:
            #print(dataset)
            #print(line[1])
        if json_line["paris_id"]:
            id = id + 1
            traceroute_dict[id] = []
            for item in json_line["result"]:
                json_subitem = item['result']
                rtt = 0
                hop_ip = "x"
                s = 0 
                for item2 in json_subitem :
                    if "from" in item2 :
                        if item2["from"] != hop_ip :
                            hop_ip = item2["from"]
                        s = s+1    
                        rtt = rtt + item2["rtt"]
                        rtt_avg = rtt/s
                if hop_ip != "x" and s != 0 :
                    rtt_avgfinal = rtt_avg
                    traceroute_dict[id].append({
                        'hop': item['hop'], 
                        'from' : hop_ip, 
                        'rtt' : rtt_avgfinal})

with open('traceroute_test.json', 'w') as fp:
        json.dump(traceroute_dict,fp)
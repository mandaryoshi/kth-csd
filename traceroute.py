#!/usr/bin/python
import json
from tqdm import tqdm


with open('../traceroutes/14092020/traceroute-2020-09-14T1100') as f:
  traceroutes = json.load(f)

id = 0
traceroute_dict = {}
for dataset in tqdm(traceroutes):
    id = id + 1
    traceroute_dict[id] = []
    for item in dataset['result']:
        rtt = 0
        hop_ip = "x"
        s = 0 
        for item2 in item['result']:
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

#print(traceroute_dict)

#useroutput=input('Enter the name of the file you want to write: ')

with open('traceroutes.json', 'w') as fp:
        json.dump(traceroute_dict,fp)

#with open(useroutput, 'w') as outfile:
#    json.dump(traceroute_dict, outfile)
#!/usr/bin/python
import json

userinput=input('Enter the name of the file you want to read: ')

json_data=[]
with open(userinput,'r') as readfile:
    for line in readfile :
        json_line = json.loads(line)
        json_data.append(json_line)

    id = 0
    traceroute_dict = {}
    for dataset in json_data:
        json_item = dataset['result']
        id = id + 1
        traceroute_dict[id] = []
        for item in json_item:
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
        #print(traceroute_dict)

    useroutput=input('Enter the name of the file you want to write: ')
    with open(useroutput, 'w') as outfile:
        json.dump(traceroute_dict, outfile) 
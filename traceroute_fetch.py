#!/usr/bin/python
import json
from tqdm import tqdm
import time





#with open('../traceroute-2020-09-14T1100') as readfile:
#    json_data = ijson.items(readfile, '')

id = 0


file_object = open('traceroute_20200914_1100', 'w')

with open('../traceroutes/14092020/traceroute-2020-09-14T1100','r') as readfile:

    for line in tqdm(readfile):
        json_line = json.loads(line)
        #for dataset in json_line:
            #print(dataset)
            #print(line[1])
        traceroute_dict = {}

        if "paris_id" in json_line and "result" in json_line:
            if json_line["paris_id"] > 0 and json_line["af"] == 4:
                id = id + 1
                traceroute_dict[id] = []
                for item in json_line["result"]:
                    rtt = 0
                    hop_ip = "x"
                    s = 0
                    if "result" in item:
                        for item2 in item["result"]:
                            if "from" in item2 and "rtt" in item2:
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
                                'rtt' : round(rtt_avgfinal)})
                file_object.write(json.dumps(traceroute_dict))
                file_object.write('\n')
        #print(traceroute_dict)
        #time.sleep(1)

#file_object.close()

#with open('traceroute_test.json', 'w') as fp:
#        json.dump(traceroute_dict,fp)

import json
from tqdm import tqdm
import time

id = 0


file_object = open('example_traceroute_results', 'w')

with open('example_traceroute','r') as readfile:

    for line in readfile:
        json_line = json.loads(line)
        traceroute_dict = {}

        if "paris_id" in json_line and "result" in json_line:
            if json_line["paris_id"] > 0 and json_line["af"] == 4:
                id = id + 1
                traceroute_dict[id] = []
                for item in json_line["result"]:
                    rtt = 0
                    hop_ip = "x"
                    if "result" in item:
                        for item2 in item["result"]:
                            if "from" in item2 and "rtt" in item2:
                                hop_ip = item2["from"]  
                                rtt = rtt + item2["rtt"]
                                rtt_avg = rtt/len(item["result"])
                        if hop_ip != "x":
                            traceroute_dict[id].append({
                                'hop': item['hop'], 
                                'from' : hop_ip, 
                                'rtt' : round(rtt_avg, 2)})
                file_object.write(json.dumps(traceroute_dict))
                file_object.write('\n')
        #print(traceroute_dict)
        #time.sleep(1)

file_object.close()

#with open('traceroute_test.json', 'w') as fp:
#        json.dump(traceroute_dict,fp)

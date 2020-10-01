import json 
import time
from tqdm import tqdm
from scripta import IxpDetector
#import timeit
#start_time = timeit.default_timer()
#print(timeit.default_timer() - start_time)

file_object = open('json_results/hop_results', 'w')

ix_detector = IxpDetector()

with open('json_results/traceroute_results','r') as readfile:
    id = 1
   
    for line in tqdm(readfile):
        json_line = json.loads(line)
        ip_array = []
        hop_array = []
        iphop_dict = {}
       	iphop_dict["id"] = id
        for i in json_line[str(id)]:
          ip_array.append(i["from"])
          hop_array.append(i["hop"])

        ixp_ip2, ixp_id = ix_detector.ixpdetection(ip_array)
    
#If an IXP ip is detected, save it along with its previous and next hop IP addresses.        
        if ixp_ip2 :
            ixp_index = ip_array.index(str(ixp_ip2))
            
            if ((ixp_index-1 >= 0) and (hop_array[ixp_index-1] == (hop_array[ixp_index] - 1))):
              if ((ixp_index+1 <= (len(ip_array)-1)) and (hop_array[ixp_index] == (hop_array[ixp_index + 1] - 1))):
                iphop_dict["data"] = {
                  'previous_hop' : ip_array[ixp_index-1],
                  'ixp_hop' : ip_array[ixp_index],
                  'next_hop' : ip_array[ixp_index+1]
                }
                file_object.write(json.dumps(iphop_dict))
                file_object.write('\n')
        id = id + 1

file_object.close()

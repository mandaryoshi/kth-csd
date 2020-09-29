from netaddr import IPNetwork, IPAddress
import json 
import time
from tqdm import tqdm
from scripta import IxpDetector

file_object = open('json_results/example_hop_results', 'w')

ix_detector = IxpDetector()

with open('json_results/example_traceroute_results','r') as readfile:
    id = 1
   
    for line in readfile:
        json_line = json.loads(line)
        ip_array = []
        iphop_dict = {}
        iphop_dict[id] = []
        for i in json_line[str(id)]:
          ip_array.append(i["from"])

        ixp_ip2, ixp_id = ix_detector.ixpdetection(ip_array)
        #print(ixp_ip2, ixp_id)
        time.sleep(1)
    
#If an IXP ip is detected, save it along with its previous and next hop IP addresses.        
        if ixp_ip2 :
            ixp_index = ip_array.index(str(ixp_ip2))
            previous_hop = ip_array[ixp_index-1] if (ixp_index-1 >= 0) else None
            current_hop = ip_array[ixp_index]
            next_hop = ip_array[ixp_index+1] if (ixp_index+1 <= (len(ip_array)-1)) else None
            
            iphop_dict[id].append({
               'previous_hop' : previous_hop,
               'ixp_hop' : current_hop,
               'next_hop' : next_hop
            })
            #print(iphop_dict)
            file_object.write(json.dumps(iphop_dict))
            file_object.write('\n')
        id = id + 1

file_object.close()
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
   
  counter = 0
  for line in tqdm(readfile):
    json_line = json.loads(line)
    for key, trace in json_line
      ip_array = []
      hop_array = []
      iphop_dict = {}
      iphop_dict["id"] = key
      for i in trace[key]:
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
              """
              counter = counter + 1
              if counter = 1000000:
                file_object.write(json.dumps(iphop_dict))
                file_object.write('\n')
                iphop_dict = {}
                counter = 0
              """
  file_object.write(json.dumps(iphop_dict))
  file_object.write('\n')
        

file_object.close()

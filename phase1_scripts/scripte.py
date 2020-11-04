import json 
import time
from tqdm import tqdm
from scripta import IxpDetector
import ujson
import sys
#import timeit
#start_time = timeit.default_timer()
#print(timeit.default_timer() - start_time)

sys.path.insert(0, '/home/csd/IK2200HT201-IXP')

date = sys.argv[1]
hour = sys.argv[2]

#change the date of the folder
output_path = "/home/csd/traceroutes/" + date + "/" + hour + "/hop_results"
file_object = open(output_path, 'w')		                              # Open the file where de dictionary is going to be dumped

info = open('json_results/ixp_info_results.json')                          # Open ixp_info file to insert it in script a) instance
ixp_info = ujson.load(info)
ix_detector = IxpDetector(ixp_info)

#change the name of the folder
input_path = "/home/csd/traceroutes/" + date + "/" + hour + "/traceroute_results"
with open(input_path,'r') as readfile:  			              # Open traceroute results file that is gonna be analyzed
  #counter = 0
  json_line = ujson.load(readfile)
  iphop_dict = {}
  for key, trace in tqdm(json_line.items()):                                  # Loop through each traceroute recorded in the dictionary
    ip_array = []
    hop_array = []
    rtt_array = []
    

    for i in trace["hops"]:                                                           # For every hop in the traceroute a IP array and hop number array are created
      ip_array.append(i["from"])                          
      hop_array.append(i["hop"])                                              # This array allows us to identify if there is any missing hops in between
      rtt_array.append(i["rtt"])

    ixp_ip2, ixp_id = ix_detector.ixpdetection(ip_array)                      # Search in the hop IP array if there is an IXP IP
  
        
    if ixp_ip2 :                                                              # If an IXP ip is detected, save it along with its previous and next hop IP addresses.
        ixp_index = ip_array.index(str(ixp_ip2))
                                                                              # Chech if the previous and next hop are actually in the correct order
        if ((ixp_index-1 >= 0) and (hop_array[ixp_index-1] == (hop_array[ixp_index] - 1))):
          if ((ixp_index+1 <= (len(ip_array)-1)) and (hop_array[ixp_index] == (hop_array[ixp_index + 1] - 1))): 
            iphop_dict[key] = {                                               # Add a new entry to the dictionary with the key being the traceroute id
              'previous_hop' : ip_array[ixp_index-1],
              'ixp_hop' : ip_array[ixp_index],
              'next_hop' : ip_array[ixp_index+1],
              'ixp_id' : ixp_id,
              'rtts' : [rtt_array[ixp_index-1], rtt_array[ixp_index]],
              'msm_id' : trace["msm_id"],
              'prb_id' : trace["prb_id"],
              'timestamp' : trace["timestamp"],
            }
            """
            counter = counter + 1
            if counter = 1000000:
              file_object.write(json.dumps(iphop_dict))
              file_object.write('\n')
              iphop_dict = {}
              counter = 0
            """
file_object.write(ujson.dumps(iphop_dict))
file_object.write('\n')
        

file_object.close()

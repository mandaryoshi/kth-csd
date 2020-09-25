from netaddr import IPNetwork, IPAddress
import json 
import time
from tqdm import tqdm


with open('Documents/ixp_test.json') as f:
  ixp_info = json.load(f)

def ixpdetection(ip_array):
  for value,ixp in ixp_info.items():
    for prefix in ixp["ipv4_prefix"]:
      for ip in ip_array:
        if IPAddress(ip) in IPNetwork(prefix):
          ixp_ip = IPAddress(ip)
          return ixp_ip
          #time.sleep(1)

file_object = open('Documents/example_hop_results', 'w')

with open('Documents/example_traceroute_results','r') as readfile:
    id = 1
   
    for line in readfile:
        json_line = json.loads(line)
        ip_array = []
        iphop_dict = {}
        iphop_dict[id] = []
        for i in json_line[str(id)]:
          ip_array.append(i["from"])  
        ixp_ip2 = ixpdetection(ip_array)
#If an IXP ip is detected, save it along with its previous and next hop IP addresses.        
        if ixp_ip2 :
            ixp_index = ip_array.index(str(ixp_ip2))
            if ixp_index-1 >= 0:
              #print("Prev Hop:", ip_array[ixp_index-1])
              previous_hop = ip_array[ixp_index-1]
            elif ixp_index-1 < 0:
              previous_hop = None
            #print("IXP Hop:", ip_array[ixp_index])
            current_hop = ip_array[ixp_index]
            if ixp_index+1 <= len(ip_array)-1 :
              #print("Next Hop:", ip_array[ixp_index+1])
              next_hop = ip_array[ixp_index+1]
            elif ixp_index+1 >= len(ip_array) :
              #print("Next Hop:", 0)
              next_hop = None
            
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
from netaddr import IPNetwork, IPAddress
import json 
import time
from tqdm import tqdm

#test = ["208.115.136.24","206.126.236.200","206.223.118.35"]

with open('ixp_test.json') as f:
  ixp_info = json.load(f)

def ixpdetection(ip_array):
  for value,ixp in ixp_info.items():
    #print(ixp["ipv4_prefix"])
    for prefix in ixp["ipv4_prefix"]:
      for ip in ip_array:
        if IPAddress(ip) in IPNetwork(prefix):
          #print(value)
          ixp_ip = IPAddress(ip)
          return ixp_ip
          time.sleep(1)

with open('example_traceroute_results','r') as readfile:
    id = 1
    for line in readfile:
        json_line = json.loads(line)
        ip_array = []

        for i in json_line[str(id)]:
          ip_array.append(i["from"])  
        ixp_ip2 = ixpdetection(ip_array)
#If an IXP ip is detected, save it along with its previous and next hop IP addresses.        
        if ixp_ip2:
            ixp_index = ip_array.index(str(ixp_ip2))
            print("Prev Hop:", ip_array[ixp_index-1])
            print("IXP Hop:", ip_array[ixp_index])
            print("Next Hop:", ip_array[ixp_index+1])
        id = id + 1

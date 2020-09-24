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
          print(value)
          time.sleep(1)

with open('traceroute_20200914_1100','r') as readfile:
    id = 1
    for line in readfile:
        json_line = json.loads(line)
        ip_array = []
        #print(json_line)
        #time.sleep(1)

        for i in json_line[str(id)]:
          ip_array.append(i["from"])
        ixpdetection(ip_array)
        id = id + 1

#ixpdetection(test)
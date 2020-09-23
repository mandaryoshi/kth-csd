from netaddr import IPNetwork, IPAddress
import json 
import time

#test = ["208.115.136.24","206.126.236.200","206.223.118.35"]

#with open('ixp_test.json') as f:
#  ixp_info = json.load(f)

with open('traceroute_20200914_1100','r') as readfile:
    id = 0
    for line in readfile:
        
        
        json_line = json.loads(line)
        ip_array = []
        print(json_line)
        time.sleep(1)

        """ for i in json_line[id]:
          ip_array.append(i["from"])
        ixpdetection(ip_array)
        id = id + 1 """


def ixpdetection(ip_array):
  for value,ixp in ixp_info.items():
    print(ixp["ipv4_prefix"])
    for prefix in ixp["ipv4_prefix"]:
      for ip in ip_array:
        if IPAddress(ip) in IPNetwork(prefix):
          print(value)

#ixpdetection(test)


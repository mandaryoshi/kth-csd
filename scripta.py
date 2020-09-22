from netaddr import IPNetwork, IPAddress
import json 


test = ["208.115.136.24","206.126.236.200","206.223.118.35"]

with open('ixp_test.json') as f:
  ixp_info = json.load(f)

def ixpdetection(ip_array):
  for value,ixp in ixp_info.items():
    print(ixp["ipv4_prefix"])
    for prefix in ixp["ipv4_prefix"]:
      for ip in ip_array:
        if IPAddress(ip) in IPNetwork(prefix):
          print(value)

ixpdetection(test)


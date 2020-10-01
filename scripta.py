from netaddr import IPNetwork, IPAddress
import json 
import time
from tqdm import tqdm
import pytricia

#test = ["208.115.136.24","206.126.236.200","206.223.118.35"]

class IxpDetector:

  def __init__(self):

    with open('json_results/ixp_info_results.json') as f:
      self.ixp_info = json.load(f)

  def ixpdetection(self, ip_array):
    pyt = pytricia.PyTricia()
    for idval,ixp in self.ixp_info.items():
      for prefix in ixp["ipv4_prefix"]:
        #print(prefix)
        pyt.insert(prefix, '')
        for ip in ip_array:
          if ip in pyt:
            return (ip, idval)
    return (None, None)        


#Ixp_detector().ixpdetection(test)



"""with open('traceroute_20200914_1100','r') as readfile:
    id = 1
    for line in readfile:
        json_line = json.loads(line)
        ip_array = []
        #print(json_line)
        #time.sleep(1)

        for i in json_line[str(id)]:
          ip_array.append(i["from"])
        ixpdetection(ip_array)
        id = id + 1"""

#ixpdetection(test)
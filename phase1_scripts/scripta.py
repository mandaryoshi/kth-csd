import json
import ujson 
import time
from tqdm import tqdm
import pytricia




class IxpDetector:

  def __init__(self):

    with open('../IK2200HT201-IXP/json_results/ixp_info_results.json') as f:
      self.ixp_info = ujson.load(f)
      self.pyt = pytricia.PyTricia()
      for idval,ixp in self.ixp_info.items():
        for prefix in ixp["ipv4_prefix"]:
          self.pyt.insert(prefix, idval)

  def ixpdetection(self, ip_array):
    for ip in ip_array:
      idval = self.pyt.get(ip)
      if idval != None:
        return (ip, idval)
    return (None, None)


#ix_detector = IxpDetector()

#ip_array = ['80.81.202.215']

#print(ix_detector.ixpdetection(ip_array))


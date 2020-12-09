import json
import ujson 
import time
from tqdm import tqdm
import pytricia


class IxpDetector:

  def __init__(self, file):                   # "file" variable is meant to be the ixp_info file extracted from script ixp_info.py
    
  
    self.pyt = pytricia.PyTricia()            # Creating a pytricia tree instance 
    for idval,ixp in file.items():
      for prefix in ixp["ipv4_prefix"]:       # Loop through all prefixes in each IXP
        self.pyt.insert(prefix, idval)        # inserting the prefix to the tree linked to it's IXP id

  def ixpdetection(self, ip_array):           # Function takes an array of IP addresses
    for ip in ip_array:       
      idval = self.pyt.get(ip)                # For each IP the get method does a lookup 
      if idval != None:                       # If the get method finds a match the IP and IXP id are returned
        return (ip, idval)
    return (None, None)                       # In case of no match found, forced to return a tuple to avoid format problems



import json
import ujson
import pytricia
import time
import sys

sys.path.insert(0, '/home/csd/IK2200HT201-IXP')


class non_IxpIP_AS_mapping:

    def __init__(self):
        with open('/home/csd/IK2200HT201-IXP/json_results/nonixp_info_results.json') as f:     # The same way as in script a) all prefixes are loaded
            self.nonixp_info = ujson.load(f)                            # into a pytricia tree.
            self.pyt = pytricia.PyTricia()
            for ip in self.nonixp_info:
                while True:
                    try: 
                        self.pyt.insert(ip, self.nonixp_info[ip])       # Linked to the prefix the ASN is added in this case
                        break
                    except ValueError:
                            break


    def mapping(self, ip):                                                 
        asn = self.pyt.get(ip)                                           # For the value introduced an IP lookup is made with the 
        if asn != None:                                                  # values inserted in the initialization and in case there 
            return (ip, asn)                                             # is a match then the IP and ASN are returned, and if none 
        return (None, None)                                              # match, a "None" value tuple is forced.

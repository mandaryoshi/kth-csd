import json
import ujson
import pytricia
import time


class non_IxpIP_AS_mapping:
    def __init__(self):
        with open('../json_results/nonixp_info_results.json') as f:
            self.nonixp_info = ujson.load(f)
            self.pyt = pytricia.PyTricia()
            for ip in self.nonixp_info:
                while True:
                    try: 
                        self.pyt.insert(ip, self.nonixp_info[ip])
                        break
                    except ValueError:
                            #print(net)
                            #print("What happened there?")
                            break


    def mapping(self, iparray):
        for ip in iparray:
            asn = self.pyt.get(ip)
            if asn != None:
                return (ip, asn)

asn = non_IxpIP_AS_mapping()
ip_array = ['185.111.204.20'] #, '185.111.204.20', '213.144.173.173']
print(asn.mapping(ip_array))
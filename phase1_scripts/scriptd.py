import json
import ujson
import pytricia



class non_IxpIP_AS_mapping:
    def __init__(self):
    with open('../json_results/nonixp_info_results.json') as f:
        self.nonixp_info = ujson.load(f)
        self.pyt = pytricia.PyTricia()
            for net in self.nonixp_info.values():
                self.pyt.insert(net["nonixpip"],net["asn"])

    def mapping(self, iparray):
        for ip in iparray:
            asn = self.pyt.get(ip)
            if asn != None:
            return (ip, asn)

#asn = non_IxpIP_AS_mapping()
#ip_array = ['1.0.0.2']
#print(asn.mapping(ip_array))
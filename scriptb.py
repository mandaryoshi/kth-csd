import json

class IxpIP_AS_mapping:
    def __init__(self):
        with open('json_results/ixp_info_results.json') as f:
           self.ixp_info = json.load(f)

    def mapping(self, ixpip):        
           for ixp in self.ixp_info.values():
               for addr,asn in ixp["net_set"].items():
                   for ip in ixpip:
                       if ip == addr:
                           return (asn)
                       

A = IxpIP_AS_mapping()
b = ["206.126.236.23", "206.126.236.117"]
print(A.mapping(b))

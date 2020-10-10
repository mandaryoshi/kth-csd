import json


class IxpIP_AS_mapping:
    def __init__(self, file):
        #with open('../json_results/ixp_info_results.json') as f:
        #    self.ixp_info = json.load(f)
        self.ixp_info = file

    def mapping(self, ixpip):
        for ixp in self.ixp_info.values():
            for addr,asn in ixp["net_set"].items():
                #for ip in ixpip:
                if ixpip == addr:
                    return (asn)

#asn = IxpIP_AS_mapping()
#print(asn.mapping('80.81.195.26'))


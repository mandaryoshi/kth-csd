


class IxpIP_AS_mapping:
    def __init__(self, file):
        #with open('json_results/ixp_info_results.json') as f:
        #    self.ixp_info = json.load(f)
        self.ixp_info = file

    def mapping(self, ixpip, ix_id):
        """for ixp in self.ixp_info.values():
            for addr,asn in ixp["net_set"].items():
                #for ip in ixpip:
                if ixpip == addr:
                    return (asn)"""
        if str(ix_id) in self.ixp_info:
            if ixpip in self.ixp_info[str(ix_id)]["net_set"]:
                return self.ixp_info[str(ix_id)]["net_set"][ixpip]


#asn = IxpIP_AS_mapping()
#print(asn.mapping("185.1.179.34", 3169))


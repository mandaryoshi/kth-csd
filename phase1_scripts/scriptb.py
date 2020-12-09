


class IxpIP_AS_mapping:
    def __init__(self, file):                                          # "file" variable is meant to be the ixp_info file extracted from script ixp_info.py
        self.ixp_info = file

    def mapping(self, ixpip, ix_id):                                   # The ix_id input is used to access directly the net_set of the IXP
                                                                       # to decrease the amount of values to compare.    
        if str(ix_id) in self.ixp_info:                                # Checking if the IXP id introduced exists in the dictionary.
            if ixpip in self.ixp_info[str(ix_id)]["net_set"]:          # Checking if the IXP IP exists inside the net_set of the IXP
                return self.ixp_info[str(ix_id)]["net_set"][ixpip]     # Return the ASN value accessed directly from the dictionary using the 2 values introduced


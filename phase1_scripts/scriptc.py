import json

class FacilityMapping:

  def __init__(self, file):                           # "file" variable is meant to be the ixp_info file extracted from script ixp_info.py

    self.ixp_info = file

  def facility_search(self, ixp_id):
    
    return self.ixp_info[str(ixp_id)]["fac_set"]      # Directly return the list of facilities for that ixp_id
                                                      # No need to check because the ixp_id introduced is also extracted from the same dictionary 


#facs = FacilityMapping()
#print(facs.facility_search(31))
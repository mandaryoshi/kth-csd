import json

class FacilityMapping:

  def __init__(self, file):

    #with open('../json_results/ixp_info_results.json') as f:
    #  self.ixp_info = json.load(f)
    self.ixp_info = file

  def facility_search(self, ixp_id):
    
    return self.ixp_info[str(ixp_id)]["fac_set"]


#facs = FacilityMapping()
#print(facs.facility_search(31))
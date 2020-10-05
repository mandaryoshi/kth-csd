import json

class FacilityMapping:

  def __init__(self):

    with open('../json_results/ixp_info_results.json') as f:
      self.ixp_info = json.load(f)

  def facility_search(self, ixp_id):
    
    return self.ixp_info[str(ixp_id)]["fac_set"]



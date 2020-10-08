"""
Part A:
    1. receive an ip (ixp_hop ) and find ixp_id in hop_results
    2. run script c to get a facility set for the ixp id  = [facIXP]
    3. find asn (script b) associated to that ixp_ip
    4. find the fac of asn in step 3 (asn_fac mapping)
    5. check the common facilities between these two  - [facIXP] and [facASN] = [facRES]

Part B:
    6. if more than one facility remains, use script f to get the neighbours of the ixp hop
    7. check the as of these neighbours using script d
    8. fetch the facilities of these as = [fac3] - [facX]
    9. check the common facilities [facRES] and [fac3 - facX]
"""
import sys
import ujson
import time
from tqdm import tqdm

sys.path.insert(0, '/home/csd/IK2200HT201-IXP')
from phase1_scripts.scriptb import IxpIP_AS_mapping
from phase1_scripts.scriptc import FacilityMapping
from phase1_scripts.scriptd import non_IxpIP_AS_mapping

#Class instances
ixp_to_asn = IxpIP_AS_mapping()
ixp_to_fac = FacilityMapping()
nonixp_to_asn = non_IxpIP_AS_mapping()

with open('../json_results/asn_fac_results.json') as f:
    asn_fac_info = ujson.load(f)

with open('../json_results/hop_results') as readfile:
    hop_results = ujson.load(readfile)
    for key, hops in tqdm(hop_results.items()):
        ixp_fac_set = ixp_to_fac.facility_search(hops["ixp_id"])
        #print(ixp_fac_set)
        #time.sleep(1)
        ixp_asn = ixp_to_asn.mapping(hops["ixp_hop"])
        if ixp_asn != None and str(ixp_asn) in asn_fac_info:
            ixp_asn_fac_set = asn_fac_info[str(ixp_asn)]
            #print(ixp_asn_fac_set)
            #time.sleep(1)
            fac_result = []
            for facility in ixp_fac_set:
                if facility in ixp_asn_fac_set:
                    fac_result.append(facility)
            #print(fac_result)
            #time.sleep(1)
#What if there is no common facility from part a itself? What does that mean?
# get the length of fac_result > 1, script f

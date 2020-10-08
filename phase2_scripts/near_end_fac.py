


"""
    1. receive an ip
    2. run script a to receive an ixp id
    3. run script c to get a facility set for the ixp id  = [facIXP]
    4. find the previous hop of that ixp ip using script e results
    5. use script d to get the AS of the previous hop
    6. fetch the facilities for that as using the as to fac results = [facPREV] 
    7. check the common facilities between these two  - [facIXP] and [facPREV] = [facRES]

    8. if more than one facility remains, use script f to get the neighbours of the previous hop
    9. check the as of these neighbours using script d
    10. fetch the facilities of these as = [fac3] - [facX]
    11. check the common facilities [facRES] and [fac3 - facX]
"""
import sys
import ujson
from tqdm import tqdm

sys.path.insert(0, '/home/csd/IK2200HT201-IXP')
from phase1_scripts.scriptc import FacilityMapping
from phase1_scripts.scriptd import non_IxpIP_AS_mapping


asn_fac = non_IxpIP_AS_mapping()
ixp_fac = FacilityMapping()

with open('../json_results/asn_fac_results.json') as f:
    asn_fac_info = ujson.load(f)

with open("../json_results/hop_results") as readfile:
    hop_results = ujson.load(readfile)
    counter = 0
    counter2 = 0
    for key, hops in tqdm(hop_results.items()):
#        print([hops["previous_hop"]])
        ixp_fac_set = ixp_fac.facility_search(hops["ixp_id"])
        ix_id, asn = asn_fac.mapping([hops["previous_hop"]])
        if asn != None and str(asn) in asn_fac_info:
            asn_fac_set = asn_fac_info[str(asn)]
            fac_match = []
            for facility_id in ixp_fac_set:
                if facility_id in asn_fac_set:
                    fac_match.append(facility_id)

            if len(fac_match) == 1:
                counter = counter + 1
            else: counter2 = counter2 + 1

    first_step_fac = (counter)*100/len(hop_results)
    multiple_fac = (counter2)*100/len(hop_results)

    print("FIRST SETP CONSTRINED FACILITIES",first_step_fac)
    print("MULTIPLE FACILITIES FOUND WHILE CONSTRAINING",multiple_fac)

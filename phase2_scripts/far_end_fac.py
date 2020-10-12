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
import collections

sys.path.insert(0, '/home/csd/IK2200HT201-IXP')
from phase1_scripts.scriptb import IxpIP_AS_mapping
from phase1_scripts.scriptc import FacilityMapping
from phase1_scripts.scriptd import non_IxpIP_AS_mapping
from phase1_scripts.scriptf import IPNeighbors

#file open 
file = open('../json_results/ixp_info_results.json')
ixp_info = ujson.load(file)

#Class instances
ixp_to_asn = IxpIP_AS_mapping(ixp_info)
ixp_to_fac = FacilityMapping(ixp_info)
nonixp_to_asn = non_IxpIP_AS_mapping()
ip_neighbors = IPNeighbors()

with open('../json_results/asn_fac_results.json') as f:
    asn_fac_info = ujson.load(f)

with open('../json_results/hop_results') as readfile:
    hop_results = ujson.load(readfile)
    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    counter5 = 0
    counter6 = 0

    for key, hops in tqdm(hop_results.items()):
        ixp_fac_set = ixp_to_fac.facility_search(hops["ixp_id"])
        #print(ixp_fac_set)
        #time.sleep(1)
        ixp_asn = ixp_to_asn.mapping(hops["ixp_hop"], hops["ixp_id"])
        if ixp_asn != None and str(ixp_asn) in asn_fac_info:
            ixp_asn_fac_set = asn_fac_info[str(ixp_asn)]
            #print(ixp_asn_fac_set)
            #time.sleep(1)
            fac_result = []
            for facility in ixp_fac_set:
                if facility in ixp_asn_fac_set:
                    fac_result.append(facility)
            if len(fac_result) == 1:
                counter1 = counter1 + 1
            elif (len(fac_result) > 1):
                counter2 = counter2 + 1

                neighbours = ip_neighbors.graphgenerator(hops["ixp_hop"])
                neighbour_fac_set = []
                neighbour_as_set = []

                for ip in neighbours:
                    ip_ip2, asn2 = nonixp_to_asn.mapping(ip)
                    if asn2 != None and (str(asn2) in asn_fac_info) and (asn2 != ixp_asn):
                         neighbour_as_set.append(asn2)

                for asnumber in neighbour_as_set:
                    neighbour_fac_set.append(asn_fac_info[str(asnumber)])

                c = 0
                if len(neighbour_fac_set) > 0:
                    flat_list = []
                    for sublist in neighbour_fac_set:
                        for fac_id in fac_result:
                            if fac_id in sublist:
                                flat_list.append(fac_id)
                    cnt = collections.Counter(flat_list)
                    new_list = []
                    for f_id, times in cnt.items():
                        if times/len(neighbour_fac_set) >= 0.75:
                            new_list.append(f_id)
                    if len(new_list) == 1:
                        counter3 = counter3 + 1
                    else:
                        counter4 = counter4 + 1

            elif (len(fac_result) == 0):
                counter5 = counter5 + 1

        else:
            counter6 = counter6 + 1

    first_step_fac = (counter1)*100/(len(hop_results))
    multiple_fac = (counter2)*100/(len(hop_results))
    last_step_fac = (counter3)*100/(len(hop_results))
    couldnotfind_fac = (counter4)*100/(len(hop_results))
    no_mapping = (counter5)*100/len(hop_results)
    no_info = (counter6)*100/len(hop_results)



    print("FIRST STEP CONSTRAINED FACILITIES",first_step_fac, counter1)
    print("MULTIPLE FACILITIES FOUND WHILE CONSTRAINING",multiple_fac, counter2)
    print("LAST STEP CONSTRAINED FACILITIES", last_step_fac, counter3)
    print("Multiple facilities remaining after last step", couldnotfind_fac, counter4)
    print("Could not find a common facility from part 1", no_mapping, counter5)
    print("Peeringdb or caida problem", no_info, counter6)


#What if there is no common facility from part a itself? What does that mean?

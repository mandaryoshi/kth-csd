import sys
import ujson
import time
from tqdm import tqdm
import collections
import matplotlib.pyplot as plt

#sys.path.insert(0, 'D:\\Documents\\IK2200HT201-IXP')
sys.path.insert(0, '/home/csd/IK2200HT201-IXP')
from phase1_scripts.scriptb import IxpIP_AS_mapping
from phase1_scripts.scriptc import FacilityMapping
from phase1_scripts.scriptd import non_IxpIP_AS_mapping
from phase1_scripts.scriptf import IPNeighbors
from phase1_scripts.scripta import IxpDetector

#file open 
file = open('../json_results/ixp_info_results.json')
ixp_info = ujson.load(file)

#Class instances
ix_detector = IxpDetector(ixp_info)
ixp_to_asn = IxpIP_AS_mapping(ixp_info)
ixp_to_fac = FacilityMapping(ixp_info)
nonixp_to_asn = non_IxpIP_AS_mapping()
ip_neighbors = IPNeighbors()

with open('../json_results/asn_fac_results.json') as f:
    asn_fac_info = ujson.load(f)

#change the name of the folder
with open('/home/csd/traceroutes/17102020/hop_results') as readfile:
    hop_results = ujson.load(readfile)
    fac_ips = {}
    counter1 = 0
    counter2 = 0
    counter3 = 0
    for key, hops in tqdm(hop_results.items()):
        ixp_fac_set = ixp_to_fac.facility_search(hops["ixp_id"])
        if len(ixp_fac_set) > 1:
            ixp_asn = ixp_to_asn.mapping(hops["ixp_hop"], hops["ixp_id"])
            if ixp_asn != None and str(ixp_asn) in asn_fac_info:
                ixp_asn_fac_set = asn_fac_info[str(ixp_asn)]
                fac_result = []
                
                for facility in ixp_fac_set:
                    if facility in ixp_asn_fac_set:
                        fac_result.append(facility)
                if len(fac_result) == 1:
                    if fac_result[0] in fac_ips:
                        if hops["ixp_hop"] not in fac_ips[fac_result[0]]:
                            fac_ips[fac_result[0]].append(hops["ixp_hop"])
                    else:
                        fac_ips[fac_result[0]] = []
                        fac_ips[fac_result[0]].append(hops["ixp_hop"])
                    counter1 = counter1 + 1
                elif (len(fac_result) > 1):
                    counter2 = counter2 + 1

                    neighbours = ip_neighbors.graphgenerator(hops["ixp_hop"])
                    neighbour_fac_set = []
                    neighbour_as_set = []
                    other_ixp_set = []
                    step3_match = []
                    
                    for ip in neighbours:
                        ip_ip2, asn2 = nonixp_to_asn.mapping(ip)
                        if asn2 != None and (str(asn2) in asn_fac_info) and (asn2 != ixp_asn):
                            neighbour_as_set.append(asn2)
                        else:
                            ixp_ip2, ixp_id = ix_detector.ixpdetection([ip])
                            if ixp_id != None:
                                other_ixp_set.append(ixp_id)

                    for ixp in other_ixp_set:
                        facilities = ixp_to_fac.facility_search(ixp)
                        for val in fac_result:
                            if val in facilities:
                                step3_match.append(val)
                    cnt2 = collections.Counter(step3_match)
                    keys2 = list(cnt2.keys())

                    if len(keys2) != 1:
                        for asnumber in neighbour_as_set:
                            neighbour_fac_set.append(asn_fac_info[str(asnumber)])

                        if len(neighbour_fac_set) > 0:
                            flat_list = []
                            for sublist in neighbour_fac_set:
                                for fac_id in fac_result:
                                    if fac_id in sublist:
                                        flat_list.append(fac_id)
                            cnt = collections.Counter(flat_list)
                            val = list(cnt.values())
                            keys = list(cnt.keys())

                            if len(val) > 1:
                                if (val[0]/len(neighbour_fac_set) >= 0.75) and (val[0] != val[1]):
                                    if keys[0] in fac_ips:
                                        if hops["ixp_hop"] not in fac_ips[keys[0]]:
                                            fac_ips[keys[0]].append(hops["ixp_hop"])
                                    else:
                                        fac_ips[keys[0]] = []
                                        fac_ips[keys[0]].append(hops["ixp_hop"])
                                    counter3 = counter3 + 1
                            elif len(val) == 1:
                                if val[0]/len(neighbour_fac_set) >= 0.75:
                                    if keys[0] in fac_ips:
                                        if hops["ixp_hop"] not in fac_ips[keys[0]]:
                                            fac_ips[keys[0]].append(hops["ixp_hop"])
                                    else:
                                        fac_ips[keys[0]] = []
                                        fac_ips[keys[0]].append(hops["ixp_hop"])
                                    counter3 = counter3 + 1   
                    else:
                        if keys2[0] in fac_ips:
                            if hops["ixp_hop"] not in fac_ips[keys2[0]]:
                                fac_ips[keys2[0]].append(hops["ixp_hop"])
                        else:
                            fac_ips[keys2[0]] = []
                            fac_ips[keys2[0]].append(hops["ixp_hop"])
                        counter3 = counter3 + 1
        elif len(ixp_fac_set) != 0:
            if ixp_fac_set[0] in fac_ips:
                if hops["ixp_hop"] not in fac_ips[ixp_fac_set[0]]:
                    fac_ips[ixp_fac_set[0]].append(hops["ixp_hop"])
            else:
                fac_ips[ixp_fac_set[0]] = []
                fac_ips[ixp_fac_set[0]].append(hops["ixp_hop"])
            counter1 = counter1 + 1    

    first_step_fac = (counter1)*100/(len(hop_results))
    multiple_fac = (counter2)*100/(len(hop_results))
    last_step_fac = (counter3)*100/(len(hop_results))

    print("FIRST STEP CONSTRAINED FACILITIES",first_step_fac, counter1)
    print("MULTIPLE FACILITIES FOUND WHILE CONSTRAINING",multiple_fac, counter2)
    print("LAST STEP CONSTRAINED FACILITIES", last_step_fac, counter3)

    counter10 = 0
    maxval = (0, 0)
    minval = (1000000, 0)
    for fac, ip_array in fac_ips.items():
        if len(ip_array) < minval[0]:
            minval = (len(ip_array), fac)
        if len(ip_array) > maxval[0]:
            maxval = (len(ip_array), fac)
        counter10 = counter10 + len(ip_array)
    #print(fac_ips[maxval[1]])
    print("max ips per fac", maxval)
    print("min ips per fac", minval)
    
    print("average ips per fac", counter10/len(fac_ips))
    print("unique facs inferred", len(fac_ips))

# 1 step = look at the ixp hop facilities in case ther's only one
# 2 step = previous hop facs compared to ixp facilities
# 3 step = from previous hop neighbour ixp hops 
# 4 step = compare non ixp neighbours to first ixp set






import sys
import ujson
from tqdm import tqdm
import time
import collections


#sys.path.insert(0, 'D:\\Documents\\IK2200HT201-IXP')
#sys.path.insert(0, '/Users/enric.carrera.aguiar/Documents/UPC/Erasmus/CSD/IK2200HT201-IXP')
sys.path.insert(0, '/home/csd/IK2200HT201-IXP')
from phase1_scripts.scriptc import FacilityMapping
from phase1_scripts.scriptd import non_IxpIP_AS_mapping
from phase1_scripts.scriptf import IPNeighbors
from phase1_scripts.scripta import IxpDetector

#file open 
file = open('../json_results/ixp_info_results.json')
ixp_info = ujson.load(file)

ip_asn = non_IxpIP_AS_mapping()
ixp_fac = FacilityMapping(ixp_info)
ip_neighbors = IPNeighbors()
ix_detector = IxpDetector(ixp_info)

with open('../json_results/asn_fac_results.json') as f:
    asn_fac_info = ujson.load(f)

#change the name of the folder
with open("/home/csd/traceroutes/14102020/hop_results") as readfile:
    hop_results = ujson.load(readfile)
    fac_ips = {}
    counter = 0
    counter2 = 0
    counter3 = 0
    for key, hops in tqdm(hop_results.items()):
        #print([hops["previous_hop"]])
        #time.sleep(1)
        ixp_fac_set = ixp_fac.facility_search(hops["ixp_id"])
        if len(ixp_fac_set) > 1:
            ip_ip, asn = ip_asn.mapping(hops["previous_hop"])
            if asn != None and str(asn) in asn_fac_info:
                asn_fac_set = asn_fac_info[str(asn)]
                fac_match = []
                for facility_id in ixp_fac_set:
                    if facility_id in asn_fac_set:
                        fac_match.append(facility_id)

                if len(fac_match) == 1:
                    if fac_match[0] in fac_ips:
                        if hops["previous_hop"] not in fac_ips[fac_match[0]]:
                            fac_ips[fac_match[0]].append(hops["previous_hop"])
                    else:
                        fac_ips[fac_match[0]] = []
                        fac_ips[fac_match[0]].append(hops["previous_hop"])
                    counter = counter + 1
                elif (len(fac_match) > 1): 
                    counter2 = counter2 + 1
                
                    neighbours = ip_neighbors.graphgenerator(hops["previous_hop"])
                    
                    other_fac_set = []
                    other_as_set = []
                    other_ixp_set = []
                    step3_match = []

                    for ip in neighbours:
                        ip_ip2, asn2 = ip_asn.mapping(ip)
                        if asn2 != None and (str(asn2) in asn_fac_info) and (asn2 != asn):
                            other_as_set.append(asn2)
                        else:
                            ixp_ip2, ixp_id = ix_detector.ixpdetection([ip])
                            if ixp_id != None:
                                other_ixp_set.append(ixp_id)

                    for ixp in other_ixp_set:
                        facilities = ixp_fac.facility_search(ixp)
                        for value in fac_match:
                            if value in facilities:
                                step3_match.append(value)
                    cnt2 = collections.Counter(step3_match)
                    keys2 = list(cnt2.keys())

                    if len(keys2) != 1:
                        for asnumber in other_as_set:
                            other_fac_set.append(asn_fac_info[str(asnumber)])

                        if len(other_fac_set) > 0:                                  
                            flat_list = []                                          
                            for sublist in other_fac_set:                           
                                for fac_id in fac_match:
                                    if fac_id in sublist:
                                        flat_list.append(fac_id)
                            cnt = collections.Counter(flat_list)
                            val = list(cnt.values())
                            keys = list(cnt.keys())

                            if len(val) > 1:
                                if (val[0]/len(other_fac_set) >= 0.75) and (val[0] != val[1]):
                                    if keys[0] in fac_ips:
                                        if hops["previous_hop"] not in fac_ips[keys[0]]:
                                            fac_ips[keys[0]].append(hops["previous_hop"])
                                    else:
                                        fac_ips[keys[0]] = []
                                        fac_ips[keys[0]].append(hops["previous_hop"])
                                    counter3 = counter3 + 1
                            elif len(val) == 1:
                                if val[0]/len(other_fac_set) >= 0.75:
                                    if keys[0] in fac_ips:
                                        if hops["previous_hop"] not in fac_ips[keys[0]]:
                                            fac_ips[keys[0]].append(hops["previous_hop"])
                                    else:
                                        fac_ips[keys[0]] = []
                                        fac_ips[keys[0]].append(hops["previous_hop"])
                                    counter3 = counter3 + 1
                    else:
                        if keys2[0] in fac_ips:
                            if hops["previous_hop"] not in fac_ips[keys2[0]]:
                                fac_ips[keys2[0]].append(hops["previous_hop"])
                        else:
                            fac_ips[keys2[0]] = []
                            fac_ips[keys2[0]].append(hops["previous_hop"])
                        counter3 = counter3 + 1
        elif len(ixp_fac_set) != 0:
            if ixp_fac_set[0] in fac_ips:
                if hops["previous_hop"] not in fac_ips[ixp_fac_set[0]]:
                    fac_ips[ixp_fac_set[0]].append(hops["previous_hop"])
            else:
                fac_ips[ixp_fac_set[0]] = []
                fac_ips[ixp_fac_set[0]].append(hops["previous_hop"])
            counter = counter + 1                        

    first_step_fac = (counter)*100/(len(hop_results))
    multiple_fac = (counter2)*100/(len(hop_results))
    last_step_fac = (counter3)*100/(len(hop_results))

    print("FIRST STEP CONSTRAINED FACILITIES",first_step_fac, counter)
    print("MULTIPLE FACILITIES FOUND WHILE CONSTRAINING",multiple_fac, counter2)
    print("LAST STEP CONTRAINED FACILITIES", last_step_fac, counter3)

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



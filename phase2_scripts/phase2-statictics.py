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
import time
import collections
import matplotlib.pyplot as plt
import numpy as np

#sys.path.insert(0, 'D:\\Documents\\IK2200HT201-IXP')
#sys.path.insert(0, '/home/csd/IK2200HT201-IXP')

#make sure to change the path
#lets check this commit!

#sys.path.insert(0, '/Users/Mandar/Documents/IK2200HT201-IXP')

from phase1_scripts.scriptc import FacilityMapping
from phase1_scripts.scriptd import non_IxpIP_AS_mapping
from phase1_scripts.scriptf import IPNeighbors
from phase1_scripts.scriptb import IxpIP_AS_mapping
from phase1_scripts.scripta import IxpDetector

values = []
values2 = []
percentages = np.arange(0, 1, 0.5)
#file open 
file = open('json_results/ixp_info_results.json')
ixp_info = ujson.load(file)

ip_asn = non_IxpIP_AS_mapping()
ixp_fac = FacilityMapping(ixp_info)
ip_neighbors = IPNeighbors()
ix_detector = IxpDetector(ixp_info)
ixp_to_asn = IxpIP_AS_mapping(ixp_info)

with open('json_results/asn_fac_results.json') as f:
    asn_fac_info = ujson.load(f)

with open("json_results/hop_results") as readfile:
    hop_results = ujson.load(readfile)
    for threshold in percentages:
        counter = 0
        counter1 = 0
        counter2 = 0
        counter3 = 0
        counter4 = 0
        for key, hops in tqdm(hop_results.items()):
            ixp_fac_set = ixp_fac.facility_search(hops["ixp_id"])
            ip_ip, asn = ip_asn.mapping(hops["previous_hop"])
            ixp_asn = ixp_to_asn.mapping(hops["ixp_hop"], hops["ixp_id"])
            if asn != None and str(asn) in asn_fac_info:
                asn_fac_set = asn_fac_info[str(asn)]
                fac_match = []
                for facility_id in ixp_fac_set:
                    if facility_id in asn_fac_set:
                        fac_match.append(facility_id)

                if len(fac_match) == 1:
                    counter = counter + 1
                elif (len(fac_match) > 1): 
                    counter2 = counter2 + 1
                
                    neighbours = ip_neighbors.graphgenerator(hops["previous_hop"])
                    
                    other_fac_set = []
                    other_as_set = []
                    other_ixp_set = []

                    for ip in neighbours:
                        ip_ip2, asn2 = ip_asn.mapping(ip)
                        if asn2 != None and (str(asn2) in asn_fac_info) and (asn2 != asn):
                            other_as_set.append(asn2)

                    for asnumber in other_as_set:
                        other_fac_set.append(asn_fac_info[str(asnumber)])

                    c = 0
                    if len(other_fac_set) > 0:                                  
                        flat_list = []                                          
                        for sublist in other_fac_set:                           
                            for fac_id in fac_match:
                                if fac_id in sublist:
                                    flat_list.append(fac_id)
                        cnt = collections.Counter(flat_list)
                        val = list(cnt.values())
                    
                        if len(val) > 1:
                            if (val[0]/len(other_fac_set) >= threshold) and (val[0] != val[1]):
                                counter3 = counter3 + 1
                        elif len(val) == 1:
                            if val[0]/len(other_fac_set) >= threshold:
                                counter3 = counter3 + 1
            
            
            if ixp_asn != None and str(ixp_asn) in asn_fac_info:
                ixp_asn_fac_set = asn_fac_info[str(ixp_asn)]

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
                        ip_ip2, asn2 = ip_asn.mapping(ip)
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
                        val = list(cnt.values())
                        if len(val) > 1:
                            if (val[0]/len(neighbour_fac_set) >= threshold) and (val[0] != val[1]):
                                counter4 = counter4 + 1
                        elif len(val) == 1:
                            if val[0]/len(neighbour_fac_set) >= threshold:
                                counter4 = counter4 + 1   
            
        values.append(counter3)
        values2.append(counter4)



#plt.plot(percentages, values)
fig, ax = plt.subplots()
ax.plot(percentages, values, label = 'near-end')
ax.plot(percentages, values2, label= 'far-end')
ax.set_title('Facilities inferred in last step for certain thresholds')
ax.set_xlabel('Threshold percentages')
ax.set_xticks(np.arange(0.1, 1, 0.05))
ax.set_ylabel('Facilities inferred')
ax.legend()
plt.grid()
plt.show()
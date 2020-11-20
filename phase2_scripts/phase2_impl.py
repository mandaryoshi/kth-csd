import sys
import ujson
from tqdm import tqdm
import time
import collections

sys.path.insert(0, '/home/csd/IK2200HT201-IXP')

from phase1_scripts.scripta import IxpDetector
from phase1_scripts.scriptb import IxpIP_AS_mapping
from phase1_scripts.scriptc import FacilityMapping
from phase1_scripts.scriptd import non_IxpIP_AS_mapping
from phase1_scripts.scriptf import IPNeighbors



# Constrained Facility Search class
class CFS:

    # Initializing all the imported files and classes from other scripts
    # hop_results: File to analyze in near-end search and far-end search
    # date and hour: Loading the correct networkx graph 
    def __init__(self, hop_results, date, hour):                                                    
        ixp_results_file = open('/home/csd/IK2200HT201-IXP/json_results/ixp_info_results.json')
        ixp_info = ujson.load(ixp_results_file)

        asn_fac_mapping_file = open('/home/csd/IK2200HT201-IXP/json_results/asn_fac_results.json')
        self.asn_fac_info = ujson.load(asn_fac_mapping_file)

        self.hop_results = hop_results

        self.ip_asn = non_IxpIP_AS_mapping()          
        self.ixp_fac = FacilityMapping(ixp_info)
        self.ip_neighbors = IPNeighbors(date, hour)
        self.ix_detector = IxpDetector(ixp_info)
        self.ixp_to_asn = IxpIP_AS_mapping(ixp_info)

        self.step1_near = 0
        self.step2_near = 0
        self.step3_near = 0
        self.step4_near = 0

        self.step1_far = 0
        self.step2_far = 0
        self.step3_far = 0
        self.step4_far = 0

    # Function to map a facility to a previous hop IP
    # Once a facility is identified, it is added to the mapping
    def prev_fac_ip_mapping(self, facs, fac_ips, hops):
        if facs[0] in fac_ips:
            if hops["previous_hop"] not in fac_ips[facs[0]]:
                fac_ips[facs[0]].append(hops["previous_hop"])
        else:
            fac_ips[facs[0]] = []
            fac_ips[facs[0]].append(hops["previous_hop"])
        pass

    # Function to map a facility to an IXP hop IP
    # Once a facility is identified, it is added to the mapping
    def ixp_fac_ip_mapping(self, facs, fac_ips, hops):
        if facs[0] in fac_ips:
            if hops["ixp_hop"] not in fac_ips[facs[0]]:
                fac_ips[facs[0]].append(hops["ixp_hop"])
        else:
            fac_ips[facs[0]] = []
            fac_ips[facs[0]].append(hops["ixp_hop"])
        pass
    

    # Function for identifying the near-end facilities
    # Returns a dictionary consisting of facilities as keys and the IPs connected to each facility
    def NearEnd(self, thld=0.75):
        fac_ips = {}

        for key, hops in tqdm(self.hop_results.items()):
            # Step 1
            ixp_fac_set = self.ixp_fac.facility_search(hops["ixp_id"])
            if len(ixp_fac_set) > 1:
                # Step 2
                ip_ip, asn = self.ip_asn.mapping(hops["previous_hop"])
                if asn != None and str(asn) in self.asn_fac_info:
                    asn_fac_set = self.asn_fac_info[str(asn)]
                    fac_match = []
                    for facility_id in ixp_fac_set:
                        if facility_id in asn_fac_set:
                            fac_match.append(facility_id)

                    #Step 2 Result
                    if len(fac_match) == 1:
                        self.prev_fac_ip_mapping(fac_match, fac_ips, hops)
                        self.step2_near = self.step2_near + 1
                    
                    # Step 3
                    elif (len(fac_match) > 1): 
                    
                        neighbours = self.ip_neighbors.graphgenerator(hops["previous_hop"])
                        
                        other_fac_set = []
                        other_as_set = []
                        other_ixp_set = []
                        step3_match = []

                        # Loop that creates 2 separate lists of neighbors
                        # One for IXPs and one for other non-IXP hops
                        for ip in neighbours:
                            ip_ip2, asn2 = self.ip_asn.mapping(ip)
                            if asn2 != None and (str(asn2) in self.asn_fac_info) and (asn2 != asn):
                                other_as_set.append(asn2)
                            else:
                                ixp_ip2, ixp_id = self.ix_detector.ixpdetection([ip])
                                if ixp_id != None:
                                    other_ixp_set.append(ixp_id)
                        
                        
                        for ixp in other_ixp_set:
                            facilities = self.ixp_fac.facility_search(ixp)
                            for value in fac_match:
                                if value in facilities:
                                    step3_match.append(value)
                        cnt2 = collections.Counter(step3_match)                 # Creating a dictionary with the ixp matches 
                        keys2 = list(cnt2.keys())                               # to have a list of unique values.

                        # Step 4
                        if len(keys2) != 1:
                            for asnumber in other_as_set:
                                other_fac_set.append(self.asn_fac_info[str(asnumber)])

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
                                    if (val[0]/len(other_fac_set) >= thld) and (val[0] != val[1]):
                                        # Step 4 Result
                                        self.prev_fac_ip_mapping(keys, fac_ips, hops)      
                                        self.step4_near = self.step4_near + 1
                                elif len(val) == 1:
                                    if val[0]/len(other_fac_set) >= thld:
                                        # Step 4 Result
                                        self.prev_fac_ip_mapping(keys, fac_ips, hops)
                                        self.step4_near = self.step4_near + 1

                        # Step 3 Result
                        else:
                            self.prev_fac_ip_mapping(keys2, fac_ips, hops)
                            self.step3_near = self.step3_near + 1


            # Step 1 Result                
            elif len(ixp_fac_set) == 1:
                self.prev_fac_ip_mapping(ixp_fac_set, fac_ips, hops)
                self.step1_near = self.step1_near + 1

        return fac_ips  

    # Function for identifying the far-end facilities
    # Returns a dictionary consisting of facilities as keys and the IPs connected to each facility                        
    def FarEnd(self, thld=0.75):

        fac_ips = {}
        
        for key, hops in tqdm(self.hop_results.items()):
            ixp_fac_set = self.ixp_fac.facility_search(hops["ixp_id"])
            # Step 1
            if len(ixp_fac_set) > 1:
                # Step 2
                ixp_asn = self.ixp_to_asn.mapping(hops["ixp_hop"], hops["ixp_id"])
                if ixp_asn != None and str(ixp_asn) in self.asn_fac_info:
                    ixp_asn_fac_set = self.asn_fac_info[str(ixp_asn)]
                    fac_result = []
                    
                    for facility in ixp_fac_set:
                        if facility in ixp_asn_fac_set:
                            fac_result.append(facility)
                    
                    # Step 2 Result
                    if len(fac_result) == 1:
                        self.ixp_fac_ip_mapping(fac_result, fac_ips, hops)
                        self.step2_far = self.step2_far + 1

                    # Step 3
                    elif (len(fac_result) > 1):

                        neighbours = self.ip_neighbors.graphgenerator(hops["ixp_hop"])
                        neighbour_fac_set = []
                        neighbour_as_set = []
                        other_ixp_set = []
                        step3_match = []
                        
                        # Loop that creates 2 separate lists of neighbors
                        # One for IXPs and one for other non-IXP hops
                        for ip in neighbours:
                            ip_ip2, asn2 = self.ip_asn.mapping(ip)
                            if asn2 != None and (str(asn2) in self.asn_fac_info) and (asn2 != ixp_asn):
                                neighbour_as_set.append(asn2)
                            else:
                                ixp_ip2, ixp_id = self.ix_detector.ixpdetection([ip])
                                if ixp_id != None:
                                    other_ixp_set.append(ixp_id)

                        for ixp in other_ixp_set:
                            facilities = self.ixp_fac.facility_search(ixp)
                            for val in fac_result:
                                if val in facilities:
                                    step3_match.append(val)
                        cnt2 = collections.Counter(step3_match)
                        keys2 = list(cnt2.keys())

                        # Step 4
                        if len(keys2) != 1:
                            for asnumber in neighbour_as_set:
                                neighbour_fac_set.append(self.asn_fac_info[str(asnumber)])

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
                                    if (val[0]/len(neighbour_fac_set) >= thld) and (val[0] != val[1]):
                                        # Step 4 Result
                                        self.ixp_fac_ip_mapping(keys, fac_ips, hops)
                                        self.step4_far = self.step4_far + 1
                                        
                                elif len(val) == 1:
                                    if val[0]/len(neighbour_fac_set) >= thld:
                                        # Step 4 Result
                                        self.ixp_fac_ip_mapping(keys, fac_ips, hops)
                                        self.step4_far = self.step4_far + 1

                        # Step 3 Result                  
                        else:
                            self.ixp_fac_ip_mapping(keys2, fac_ips, hops)
                            self.step3_far = self.step3_far + 1

            # Step 1 Result                
            elif len(ixp_fac_set) == 1:
                self.ixp_fac_ip_mapping(ixp_fac_set, fac_ips, hops)
                self.step1_far = self.step1_far + 1

        return fac_ips                 

# Example code to run:

# cfs = CFS(hop_results)
# near_end_map = cfs.NearEnd()
# far_end_map = cfs.FarEnd()

# print("near end facs", len(near_end_map))
# print("far end facs", len(far_end_map))

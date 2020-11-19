import sys
import networkx as nx
import matplotlib.pyplot as plt
import folium

sys.path.insert(0, '/home/csd/IK2200HT201-IXP')
#sys.path.insert(0, 'D:\\Documents\\IK2200HT201-IXP')

from phase2_scripts.phase2_impl import *

# Input the date and hour for applying the CFS
# Date format = 2020-10-20
# Hour format = 1800
date = sys.argv[1]
hour = sys.argv[2]

# Input of facility coordinates for map creation
coordinates = ujson.load(open("json_results/fac_loc_results.json"))

# Input of hop results to analyse
input_path = "/home/csd/traceroutes/" + date + "/" + hour + "/hop_results"
hop_result_file = open(input_path)
hop_results = ujson.load(hop_result_file)

# Conduct the CFS methodology for the hop results
cfs = CFS(hop_results, date, hour)

# Creating the world map using the folium library
m = folium.Map(
    world_copy_jump=False,
    no_wrap=False
)

# Function for the forwarding model
def forwarding_model(cfs, hop_results, m, date, hour):
    # Execute near-end and far-end facility search
    map1 = cfs.NearEnd()     
    map2 = cfs.FarEnd()

    facilities = {**map1, **map2}               # Merging of the two facility maps to have a list of 
    facilities = list(facilities.keys())        # total unique facilities identified

    # Loop to add all the facilities to the map using the coordinates 
    # Extracted from PeeringDB
    for facility in facilities:
        if str(facility) in coordinates:
            folium.Marker(
                location=(coordinates[str(facility)]["latitude"], coordinates[str(facility)]["longitude"]),
                popup=folium.Popup(html=coordinates[str(facility)]["name"], max_width='400')
            ).add_to(m)
    
    # Creating a reverse mapping from IP --> Facility to Facility --> IP 
    # This is done for both the near end and far end facilities
    near_end_map = {}
    near_end_list = []
    for fac, ips in map1.items():
        for x in ips:
            if x in near_end_map:
                near_end_list.append(x)
            else:    
                near_end_map[x] = fac
    
    # Delete IPs with more than one facility attached to them
    near_end_list = list(dict.fromkeys(near_end_list))              
    for item in near_end_list:
        del near_end_map[item]

    far_end_map = {}        
    far_end_list = []
    for fac, ips in map2.items(): 
        for x in ips:
            if x in far_end_map:
                far_end_list.append(x)
            else:
                far_end_map[x] = fac
    
    far_end_list = list(dict.fromkeys(far_end_list))
    for item in far_end_list:
        del far_end_map[item]
    

    # Start of the forwarding model
    # Forwarding dict will contain the usage for that hour bin of all the links found in the previous facility search
    fwd_dict = {}

    counter = 0
    # This list is used to create the connections between facilities in the map
    link_list = []

    for key, hops in tqdm(hop_results.items()):
        if (hops["previous_hop"] in near_end_map) and (hops["ixp_hop"] in far_end_map):

            # Creating a list for the map creation
            if (near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]]) not in link_list:         # MAP
                link_list.append((near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]]))        # MAP

            counter = counter + 1

            # calculate the rtt diff that will be used in the rtt anomaly detection
            rtt_diff = hops["rtts"][1] - hops["rtts"][0]

            # If the link is not yet in the dictionary, create a new entry with the arrays, otherwise we 
            # just append directly to the existing arrays
            if (near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]]) not in fwd_dict:
                fwd_dict[(near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]])] = {
                    "rtts": [rtt_diff],
                    "probes": [hops["prb_id"]],
                    "msm_id": [hops["msm_id"]]
                }
            else:

                fwd_dict[(near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]])]["rtts"].append(rtt_diff)
                fwd_dict[(near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]])]["msm_id"].append(hops["msm_id"])
                # Only append a new probe_id if it's not already in the list, this way the list will be of unique values
                if hops["prb_id"] not in fwd_dict[(near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]])]["probes"]:
                    fwd_dict[(near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]])]["probes"].append(hops["prb_id"])
    # With the list of links mentioned above, they are added to the existing map with all the facility locations
    for x in link_list:
        if str(x[0]) in coordinates and str(x[1]) in coordinates:
            folium.PolyLine(
                [(coordinates[str(x[0])]["latitude"], coordinates[str(x[0])]["longitude"]), 
                (coordinates[str(x[1])]["latitude"], coordinates[str(x[1])]["longitude"])],
                color="red", weight=1, opacity=1).add_to(m)
    
    print('length of near-end-map', len(near_end_map))
    print('length of far-end-map', len(far_end_map))
    print('length of fwd dict: ', len(fwd_dict))
    print('list of actual links: ', counter)
    map_path = "/home/csd/traceroutes/" + date + "/" + hour + "/map" + date + hour + ".html"    
    m.save(map_path)
    forwarding_model_path = "/home/csd/traceroutes/" + date + "/" + hour + "/connections"
    with open(forwarding_model_path, 'w') as fp:
        ujson.dump(fwd_dict,fp)
 
forwarding_model(cfs, hop_results, m, date, hour)

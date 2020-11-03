import sys
import networkx as nx
import matplotlib.pyplot as plt
import folium

date = sys.argv[1]
hour = sys.argv[2]

#sys.path.insert(0, 'D:\\Documents\\IK2200HT201-IXP')
#sys.path.insert(0, '/Users/enric.carrera.aguiar/Documents/UPC/Erasmus/CSD/IK2200HT201-IXP')
sys.path.insert(0, '/home/csd/IK2200HT201-IXP')

from phase2_scripts.phase2_impl import *

coordinates = ujson.load(open("json_results/fac_loc_results.json"))

#change the name of the folder
input_path = "/home/csd/traceroutes/" + date + "/" + hour + "/hop_results"
hop_result_file = open(input_path)
hop_results = ujson.load(hop_result_file)

cfs = CFS(hop_results, date, hour)

m = folium.Map(
    world_copy_jump=False,
    no_wrap=False
)


def forwarding_model(cfs, hop_results, m, date, hour):
    map1 = cfs.NearEnd()
    map2 = cfs.FarEnd()

    facilities = {**map1, **map2}
    facilities = list(facilities.keys())

    no_info = 0
    for facility in facilities:
        if str(facility) in coordinates:
            folium.Marker(
                location=(coordinates[str(facility)]["latitude"], coordinates[str(facility)]["longitude"]),
                popup=folium.Popup(html=coordinates[str(facility)]["name"], max_width='400')
            ).add_to(m)
        else:
            no_info = no_info + 1
    
    
    
    near_end_map = {}
    for fac, ips in map1.items():
        for x in ips:
            near_end_map[x] = fac
            
    far_end_map = {}        
    for fac, ips in map2.items():
        for x in ips:
            far_end_map[x] = fac
    

    fwd_dict = {}

    counter = 0
    link_list = []
    
    for key, hops in tqdm(hop_results.items()):
        if (hops["previous_hop"] in near_end_map) and (hops["ixp_hop"] in far_end_map):

            if (near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]]) not in link_list:
                link_list.append((near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]]))

            counter = counter + 1

            if (near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]]) not in fwd_dict:
                fwd_dict[(near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]])] = 1
            else:
                fwd_dict[(near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]])] = fwd_dict[(near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]])] + 1
    
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
    print('facilities without coordinates identified: ', no_info)
    map_path = "/home/csd/traceroutes/" + date + "/" + hour + "/map.html"    
    m.save(map_path)
    forwarding_model_path = "/home/csd/traceroutes/" + date + "/" + hour + "/connections"
    with open(forwarding_model_path, 'w') as fp:
        ujson.dump(fwd_dict,fp)
 
forwarding_model(cfs, hop_results, m, date, hour)



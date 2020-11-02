import sys
import networkx as nx
import matplotlib.pyplot as plt

sys.path.insert(0, 'D:\\Documents\\IK2200HT201-IXP')
#sys.path.insert(0, '/Users/enric.carrera.aguiar/Documents/UPC/Erasmus/CSD/IK2200HT201-IXP')
#sys.path.insert(0, '/home/csd/IK2200HT201-IXP')

from phase2_scripts.phase2_impl import *

#change the name of the folder
hop_result_file = open("json_results/hop_results")
hop_results = ujson.load(hop_result_file)

cfs = CFS(hop_results)




def forwarding_model(cfs, hop_results):
    map1 = cfs.NearEnd()
    map2 = cfs.FarEnd()
    
    graph = nx.DiGraph()

    near_end_map = {}
    for fac, ips in map1.items():
        for x in ips:
            near_end_map[x] = fac
            
    far_end_map = {}        
    for fac, ips in map2.items():
        for x in ips:
            far_end_map[x] = fac
    

    #fwd_dict = {}
    edges = []

    counter = 0

    for key, hops in tqdm(hop_results.items()):
        if (hops["previous_hop"] in near_end_map) and (hops["ixp_hop"] in far_end_map):
            #print(str(near_end_map[hops["previous_hop"]]) + "  :  " + str(far_end_map[hops["ixp_hop"]]))
            #time.sleep(0.2)
            counter = counter + 1
            edges.append((near_end_map[hops["previous_hop"]], far_end_map[hops["ixp_hop"]]))
    print(counter)
    graph.add_edges_from(edges)
    nx.draw(graph, with_labels = True)
    plt.show()

        
    
        

forwarding_model(cfs, hop_results)
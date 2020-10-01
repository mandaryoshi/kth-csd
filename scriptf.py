import json 
import time
from tqdm import tqdm
import ujson
import networkx as nx
import matplotlib.pyplot as plt

def graphgenerator(ip, graph):
    with open('json_results/traceroute_results','r') as readfile:
        id = 1
        neighbours = []
        for line in tqdm(readfile):
            json_line = ujson.loads(line)

            ip_hops = json_line[str(id)]


            for hop in ip_hops:
                hop_index = ip_hops.index(hop)
                if (hop["from"] == ip) and ((hop_index+1) <= (len(ip_hops)-1)) and ((hop["hop"] + 1) == ip_hops[hop_index + 1]["hop"]):
                    neighbours.append(ip_hops[hop_index + 1]["from"])
                    
            id = id + 1

        
        edges_array = []

        neighbours = list(dict.fromkeys(neighbours))
        for ips in neighbours:
            edges_array.append((ip, ips))

        #graph.add_node()
        #graph.add_nodes_from(neighbours)
        graph.add_edges_from(edges_array)
        #nx.draw(graph, with_labels = True)

        #print(neighbours)
        #print(edges_array)
        #plt.show()



with open('json_results/hop_results','r') as readfile:
    
    graph = nx.Graph()
    count = 0

    for line in tqdm(readfile):
        json_line = json.loads(line)

        #print(json_line["data"]["previous_hop"])
        #time.sleep(1)

        graphgenerator(json_line["data"]["previous_hop"], graph)
        count = count+1
        if count == 3:
            break
    #search through traceroutes with this ip
    nx.draw(graph, with_labels = True)
    plt.show()



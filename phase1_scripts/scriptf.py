import json 
import time
from tqdm import tqdm
import ujson
import networkx as nx
import matplotlib.pyplot as plt
import pathlib

class IPNeighbors:

    def __init__(self):
        print(pathlib.Path.cwd())
        self.trace_graph = nx.read_gpickle('network_diagram/traceroute_graph.gpickle')
        
    def graphgenerator(self, ip):
        neighbors = list(self.trace_graph.neighbors(ip))
        print(neighbors)
        return neighbors
        
        
"""
with open('json_results/hop_results','r') as readfile:
    trace_graph = nx.read_gpickle('network_diagram/traceroute_graph.gpickle')
    graph = nx.Graph()

    hop_results = ujson.load(readfile)
    count = 0
    for key, hops in tqdm(hop_results.items()):
        
        neighbors = trace_graph.neighbors(hops["previous_hop"])
        edges = []
        for neighbor in neighbors:
            edges.append((hops["previous_hop"], neighbor))
            graph.add_edges_from(edges)
        count = count + 1
        if count == 3:
            break
    nx.draw(graph, with_labels = True)
    plt.show()
"""

ip_neighbors = IPNeighbors()
ip_neighbors.graphgenerator('80.81.202.215')



import json
from tqdm import tqdm
import time
import ujson
import networkx as nx
import pickle

id = 0

graph = nx.DiGraph()
file_object = open('json_results/traceroute_results', 'w')

with open('/home/csd/traceroutes/14092020/traceroute-2020-09-14T1100','r') as readfile:
    #counter = 0
    traceroute_dict = {}
    edges_tuple = []
    for line in tqdm(readfile):
        json_line = ujson.loads(line)
        
        if "paris_id" in json_line and "result" in json_line:
            if json_line["paris_id"] > 0 and json_line["af"] == 4:

                id = id + 1
                traceroute_dict[id] = []
                edge_array = []
                for item in json_line["result"]:
                    rtt = 0
                    hop_ip = "x"
                    if "result" in item:
                        for item2 in item["result"]:
                            if "from" in item2 and "rtt" in item2:
                                hop_ip = item2["from"]
                                rtt = rtt + item2["rtt"]
                                rtt_avg = rtt/len(item["result"])
                        edge_array.append(hop_ip)
                        if hop_ip != "x":
                            traceroute_dict[id].append({
                                'hop': item['hop'], 
                                'from' : hop_ip, 
                                'rtt' : round(rtt_avg, 2)})
                    """counter = counter + 1
                    if counter == 1000000:
                        file_object.write(ujson.dumps(traceroute_dict))
                        file_object.write('\n')
                        tracereoute_dict = {}
                        counter = 0"""
        #edges_tuple = []
        for x in range(len(edge_array)):
            if x < len(edge_array) - 1:
                if edge_array[x] != "x" and edge_array[x+1] != "x":
                    edges_tuple.append((edge_array[x],edge_array[x+1]))
    graph.add_edges_from(edges_tuple)

    file_object.write(ujson.dumps(traceroute_dict))
    file_object.write('\n')
    nx.write_gpickle(graph, '../IK2200HT201-IXP/network_diagram/network_diagram/traceroute_graph.gpickle')
    
file_object.close()


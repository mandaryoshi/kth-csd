import json
from tqdm import tqdm
import time
import ujson
import networkx as nx
import pickle
import sys

date = sys.argv[1]
hour = sys.argv[2]

id = 0

graph = nx.DiGraph()

#change the name of the folder
folder_path = "/home/csd/traceroutes/" + date + "/" + hour + "/traceroute_results"
file_object = open(folder_path, 'w')

#change the name of the folder
trace_file_path = "/home/csd/traceroutes/" + date + "/" + hour + "/traceroute-" + date + "T" + hour
with open(trace_file_path,'r') as readfile:
    #counter = 0
    traceroute_dict = {}
    edges_tuple = []
    for line in tqdm(readfile):
        json_line = ujson.loads(line)
        edge_array = []
        if "paris_id" in json_line and "result" in json_line:
            if json_line["paris_id"] > 0 and json_line["af"] == 4:

                id = id + 1
                traceroute_dict[id] = []
        #        edge_array = []
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
    #change the name of the folder
    graph_path = "/home/csd/traceroutes/" + date + "/" + hour + "/traceroute_graph.gpickle"
    nx.write_gpickle(graph, graph_path)
    
file_object.close()


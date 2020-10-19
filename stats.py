import ujson
import time
import json 
import requests
import networkx as nx
import matplotlib.pyplot as plt

#IXP statistics


fd = open('json_results/ixp_info_results.json')
ixp_info = ujson.load(fd)

total_asn = []
total_fac = []
asns = []
facs = []

for key in ixp_info:
    for value in ixp_info[key]["net_set"]:
        if ixp_info[key]["net_set"][value] not in asns:
            asns.append(ixp_info[key]["net_set"][value])
    total_asn.append(len(ixp_info[key]["net_set"]))
    for value in ixp_info[key]["fac_set"]:
        facs.append(value)
    total_fac.append(len(ixp_info[key]["fac_set"]))


#asns = list(dict.fromkeys(asns))
facs = list(dict.fromkeys(facs))


print('Total exchanges: ',len(ixp_info))
print('unique asns from ixpinfo: ', len(asns))
print('unique facs from ixpinfo: ',len(facs))
print('Connections to exchanges: ',sum(total_asn))

print('Total facs from ixpinfo: ',sum(total_fac))

print('\n')


#Graph Statistics

"""

graph = nx.read_gpickle('network_diagram/traceroute_graph.gpickle')

print(graph.number_of_nodes())
print(graph.size())

options = {
    "node_color": "blue",
    "node_size": 0.01,
    "edge_color": "gray",
    "linewidths": 0,
    "width": 0.1,
}
nx.draw(graph, **options)
plt.show()


"""

#ASN-FAC statistics


fd = open('json_results/asn_fac_results.json')
asn_fac_info = ujson.load(fd)

total_fac = []
total_asns = []

for key in asn_fac_info:
    total_fac.append(asn_fac_info[key])
    total_asns.append(key)

flat_list = []
for sublist in total_fac:
    for item in sublist:
        flat_list.append(item)

print('Connections to facilities: ', len(flat_list))

total_fac = list(dict.fromkeys(flat_list))

print('Total unique ASNS from asn_fac_info: ', len(asn_fac_info))
print('Total unique facilities: ', len(total_fac))


print('\n')

new_asns = total_asns + asns
new_facs = total_fac + facs

new_asns = list(dict.fromkeys(new_asns))
new_facs = list(dict.fromkeys(new_facs))

print('total asns across ixp info and asn-fac mapping:', len(new_asns))
print('total facs across ixp info and asn-fac mapping:', len(new_facs))


print('\n')

response = requests.get("https://peeringdb.com/api/fac")
facilities = json.loads(response.text)

print('len of facs from pdb', len(facilities["data"]))

print('\n')
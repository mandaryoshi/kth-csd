import sys
import ujson
import matplotlib.pyplot as plt
import time
sys.path.insert(0,"/home/csd/IK2200HT201-IXP")
from phase2_scripts.phase2_impl import *

date = "17102020"
hour = ""

hop_results_file = open("/home/csd/traceroutes/" + date + hour + "/hop_results")
hop_results = ujson.load(hop_results_file)

cfs = CFS(hop_results, date, hour)

map1 = cfs.NearEnd()
#print("Near End IPs", map1)
map2 = cfs.FarEnd() 
#print("Far End IPs", map2)

#traceroute_results_file = open("/home/csd/traceroutes/17102020/traceroute_results")
#traceroute_results = ujson.load(traceroute_results_file)
rtt_array=[]
#new_map1 ={}

near_end_map = {}
for fac, ips in map1.items():  
    for x in ips:
        near_end_map[x] = fac
#print(near_end_map)

far_end_map = {}
for fac, ips in map2.items():
    for x in ips:
        far_end_map[x] = fac

fac_rtt_dict = {}
for key, hops in tqdm(hop_results.items()):
    if (hops["previous_hop"] in near_end_map) and (hops["ixp_hop"] in far_end_map):
        ne_fac = near_end_map[hops["previous_hop"]]
        fe_fac = far_end_map[hops["ixp_hop"]]
        rtt_diff = hops["rtts"][1] - hops["rtts"][0]
        #rtt_array.append(round(rtt_diff,2))

        fac_rtt_dict[(ne_fac, fe_fac)] = round(rtt_diff,2)

time.sleep(1)
print(fac_rtt_dict)


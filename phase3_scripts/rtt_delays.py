import sys
import ujson
import matplotlib.pyplot as plt
sys.path.insert(0,"/home/csd/IK2200HT201-IXP")
from phase2_scripts.phase2_impl import *

hop_results_file = open("/home/csd/traceroutes/17102020/hop_results")
hop_results = ujson.load(hop_results_file)

cfs = CFS(hop_results)

map1 = cfs.NearEnd()
#print("Near End IPs", map1)
map2 = cfs.FarEnd()
#print("Far End IPs", map2)

traceroute_results_file = open("/home/csd/traceroutes/17102020/traceroute_results")
traceroute_results = ujson.load(traceroute_results_file)
rtt_array=[]
#new_map1 ={}

near_end_map = {}
for fac, ips in map1.items():
    for x in ips:
        near_end_map[x] = fac

far_end_map = {}
for fac, ips in map2.items():
    for x in ips:
        far_end_map[x] = fac

for key, hops in tqdm(hop_results.items()):
    if (hops["previous_hop"] in near_end_map) and (hops["ixp_hop"] in far_end_map):
        rtt_diff = hops["rtts"][1] - hops["rtts"][0]
        rtt_array.append(round(rtt_diff,2))
print(rtt_array)


"""with open("/home/csd/traceroutes/17102020/hop_results") as readfile:
    hop_results = ujson.load(readfile)
    rtt_array_diff = []
    for key,hops in (hop_results.items()):
        rtt_diff = hops["rtts"][1] - hops["rtts"][0]
        #print(rtt_diff)
        rtt_array_diff.append(round(rtt_diff,2))
    print(rtt_array_diff)
    font_size = 10
    plt.hist(rtt_array_diff,bins=100, color='b')
    #ax.set_title('Histogram Plot of RTT Delays', fontsize=font_size)
    plt.xlabel('RTT Values', fontsize=font_size)
    plt.ylabel('Total Observations', fontsize=font_size)
    plt.tick_params(axis='both', which='major', labelsize=font_size-2)
    plt.tick_params(axis='both', which='minor', labelsize=font_size-4)
    plt.tight_layout()
    plt.show()"""

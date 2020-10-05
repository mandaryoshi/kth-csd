import ujson 
from scripta import IxpDetector
from tqdm import tqdm

ix_detector = IxpDetector()
counter = 0
with open('../json_results/hop_results', 'r') as readfile:
    
    hop_results = ujson.load(readfile)

    for key, hops in tqdm(hop_results.items()):

        ixp_ip, ixp_id = ix_detector.ixpdetection([hops["next_hop"]])
        if ixp_ip:
            counter = counter + 1

print("PERCENTAGE OF CONSECUTIVE IXPs: " + str(round((counter/len(hop_results))*100, 3)) + "%")
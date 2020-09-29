import json 
import time
from tqdm import tqdm

with open('json_results/example_hop_results','r') as readfile:
    
    for line in readfile:
        json_line = json.loads(line)

        for i in json_line:
            print(json_line[str(i)])
            print(json_line[str(i)][0])
            print(json_line[str(i)][0]["previous_hop"])
        
    #search through traceroutes with this ip
        id = 1
        with open('json_results/example_traceroute_results','r') as readfile2:
            for line2 in readfile2:
                json_line2 = json.loads(line2)
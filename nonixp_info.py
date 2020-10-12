import json
from tqdm import tqdm
import time

filename = '../json_results/routeviews-rv2-20201005-1200.pfx2as'

#nonixpip dictionary
dict1 = {}

fields = ['IP prefix','asn']

#Creating dictionary for ip
with open(filename) as fp:
    for line in tqdm(fp):
        #Readling line by line from text file
        describe = list(line.strip().split(None,2))
        describe[0] = describe[0] + '/' + describe[1]
        dict1[describe[0]] = describe[2]

output_file = open("../json_results/nonixp_info_results.json", "w")
json.dump(dict1, output_file, indent = 4)

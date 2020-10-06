import json

filename = 'json_results/example_nonixp.txt'

dict1 = {}

fields = ['nonixpip','prefix_len','asn']

#Creating dictionary for ip
with open(filename) as fp:
    l=1
    for line in fp:
        #Readling line by line from text file
        description = list(line.strip().split(None,3))
        print(description)


with open('json_results/nonixp_info_results.json', 'w') as fp:
json.dump(dict1, fp)
import json 
import requests
from tqdm import tqdm

# Sending get request and saving the response as response object
response = requests.get("https://peeringdb.com/api/netfac")

# Parsing response
netfac = json.loads(response.text)

# Defining an empty dictionary
dictionary = {

# Iterating over key-'data' to map the asn and facility ids sequentially and append the facility ids in a list.
for i in tqdm(netfac["data"]):
    if i["local_asn"] in dictionary:
        dictionary[i["local_asn"]].append(i["fac_id"])
    else:
        dictionary[i["local_asn"]] = []
        dictionary[i["local_asn"]].append(i["fac_id"])

# Opens the file where dictionary will be dumped
with open('json_results/asn_fac_results.json', 'w') as fp:
        json.dump(dictionary,fp)
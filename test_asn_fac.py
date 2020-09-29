import json 
import requests
from tqdm import tqdm

response = requests.get("https://peeringdb.com/api/netfac")

netfac = json.loads(response.text)

dictionary = {}

for i in tqdm(netfac["data"]):
    if i["local_asn"] in dictionary:
        dictionary[i["local_asn"]] = []
        dictionary[i["local_asn"]].append(i["fac_id"])
    else:
        dictionary[i["local_asn"]].append(i["fac_id"])

with open('ixp_asn_fac.json', 'w') as fp:
        json.dump(dictionary,fp)
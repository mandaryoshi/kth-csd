import ujson 
import requests
from tqdm import tqdm

response = requests.get("https://peeringdb.com/api/fac")

netfac = ujson.loads(response.text)

dictionary = {}

for i in tqdm(netfac["data"]):
    if i["latitude"] != None and i["longitude"] != None:
        dictionary[i["id"]]  =  {
            "latitude" : i["latitude"],
            "longitude" : i["longitude"],
            "name" : i["name"]
        }
       

with open('json_results/fac_loc_results.json', 'w') as fp:
        ujson.dump(dictionary,fp)
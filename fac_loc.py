import ujson 
import requests
from tqdm import tqdm

# Sending get request and saving the response as response object
response = requests.get("https://peeringdb.com/api/fac")

# Parsing response
netfac = ujson.loads(response.text)

# Defining an empty dictionary
dictionary = {}

# Iterating over key-'data' sequentially to map the facility ids with their latitude, longitude and name
for i in tqdm(netfac["data"]):
    if i["latitude"] != None and i["longitude"] != None:
        dictionary[i["id"]]  =  {
            "latitude" : i["latitude"],
            "longitude" : i["longitude"],
            "name" : i["name"],
            "city" : i["city"]
        }
       
# Opens the file where dictionary will be dumped
with open('json_results/fac_loc_results.json', 'w') as fp:
        ujson.dump(dictionary,fp)
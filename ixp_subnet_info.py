import json
import requests

response = requests.get("https://peeringdb.com/api/ixlan?depth=2")
facilities = json.loads(response.text)

print(facilities == response.json())

print(type(facilities))

dictionary = {}
dictionary["id"] = []

print(dictionary)

for i in facilities["data"]:
    if i["ixpfx_set"]:
        for j in i["ixpfx_set"]:
            if j["protocol"] == "IPv4":
                print(j["prefix"])
                dictionary2 = {}
                dictionary2["ix_id"] = i["ix_id"]
                dictionary2["ipv4_prefix"] = j["prefix"]
                dictionary["id"].append(dictionary2)

                #create a dictionary here with the values we found
                #we want id, ix_id, ipv4 prefix
                #{"id": [{"ix_id": "xyz", "ipv4_prefix": "xyz"}, {"ix_id": "xyz", "ipv4_prefix": "xyz"}]}


print(dictionary)
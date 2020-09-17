import json
import requests
#import netaddr
#import ipaddress

#ask how often peeringdb changes


response = requests.get("https://peeringdb.com/api/ixlan?depth=2")
response2 = requests.get("https://peeringdb.com/api/netixlan")



facilities = json.loads(response.text)
netixlan = json.loads(response2.text)

#print(facilities == response.json())

#print(type(facilities))

dictionary = {}


dictionary["id"] = []

for i in facilities["data"]:
    if i["ixpfx_set"]:
        for j in i["ixpfx_set"]:
            if j["protocol"] == "IPv4":
                print(j["prefix"])
                dictionary2 = {}
                dictionary2["ix_id"] = i["ix_id"]
                dictionary2["ipv4_prefix"] = j["prefix"]
                dictionary2["net_set"] = []
                for k in i["net_set"]:
                    dictionary3 = {}
                    dictionary3["asn"] = k["asn"]
                    for l in netixlan["data"]: 
                        if l["asn"] == k["asn"] and l["ix_id"] == i["ix_id"]:
                            #print("asn detected")
                            dictionary3["ipaddr4"] = l["ipaddr4"]
                            break
                    dictionary2["net_set"].append(dictionary3)
                dictionary["id"].append(dictionary2)

                #create a dictionary here with the values we found
                #we want id, ix_id, ipv4 prefix
                #{"id": [{"ix_id": "xyz", "ipv4_prefix": "xyz"}, {"ix_id": "xyz", "ipv4_prefix": "xyz"}]}


print(dictionary)

with open('ixp.json', 'w') as fp:
        json.dump(dictionary,fp)
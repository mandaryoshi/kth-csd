import json 
import requests
from tqdm import tqdm

response = requests.get("https://peeringdb.com/api/ixlan?depth=2")
response2 = requests.get("https://peeringdb.com/api/netixlan")
response3 = requests.get("https://peeringdb.com/api/ixfac")

ixpfx = json.loads(response.text)
netixlan = json.loads(response2.text)
ixpfac = json.loads(response3.text)

dictionary = {}

for i in tqdm(ixpfx["data"]):
    if i["ixpfx_set"]:
        for j in i["ixpfx_set"]:
            if j["protocol"] == "IPv4":

                dictionary2 = {}
                dictionary2["ipv4_prefix"] = j["prefix"]
                dictionary2["net_set"] = []

                x = 0
                for k in i["net_set"]:
                    #Dictionary containing the info from the all ASN connected to the IXP // Contains an array of asn_id & IPv4 addr
                    #dictionary3["asn"] = k["asn"]
                    for l in netixlan["data"]: 

                        dictionary3 = {}
                        if l["asn"] == k["asn"] and l["ix_id"] == i["ix_id"] and x != l["id"]:
                            #print("asn detected")
                            dictionary3[k["asn"]] = l["ipaddr4"]
                            dictionary2["net_set"].append(dictionary3)
                            x = l["id"]
                            break
                    #dictionary2["net_set"].append(dictionary3)

                dictionary2["fac_set"] = []

                for y in ixpfac["data"]:
                    if y["ix_id"] == i["ix_id"]:
                        dictionary2["fac_set"].append(y["fac_id"])
                dictionary[i["ix_id"]] = dictionary2
                
                
                #create a dictionary here with the values we found
                #we want id, ix_id, ipv4 prefix
                #{"id": [{"ix_id": "xyz", "ipv4_prefix": "xyz"}, {"ix_id": "xyz", "ipv4_prefix": "xyz"}]}


#print(dictionary)

with open('ixp_test.json', 'w') as fp:
        json.dump(dictionary,fp)




def find_key_for_value(d, value):
    for k, v in d.iteritems():
        if v == value:
            return k
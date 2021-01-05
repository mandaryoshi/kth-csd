import json 
import collections
import numpy as np

cities = json.load(open("json_results/fac_loc_results.json"))

locations = []

for city in cities.values():
    locations.append(city["city"])

cnter = dict(sorted(collections.Counter(locations).items(), key=lambda x: x[1], reverse=True))
print(cnter.values())


x = 1
for city , cnt in cnter.items():
    if x <= 10:
        print("TOP " + str(x) + " is " + city + " => " + str(cnt))
        x = x + 1


import json

with open('ixp_test.json') as f:
  ixp_info = json.load(f)


def facility_search(ixp_id):
    print(ixp_info[str(ixp_id)]["fac_set"])


facility_search(26)
import json


class IxpIP_AS_mapping:
    def __init__(self):
        with open('../json_results/ixp_info_results.json') as f:
            self.ixp_info = json.load(f)
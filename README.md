# Identifying Network Disruptions Affecting Colocation Facilities

We will use the RIPE Atlas platform to monitor peering interconnections established over IXP links that assist the traffic exchange of networks in colocation data centers.  We will analyze traceroute measurements performed on an Internet wide scale, build an anomaly detection tool that monitors the public peering links we identify, and report cases where the signal we extracted deviates from normal.

## Installation

Use the following 

```bash
pip install tqdm
pip install pytricia
pip install ujson
pip install networkx
pip install matplotlib
```

## Usage

First run these scripts to get traceroute and ixp info from a RIPE Atlas traceroute dump and PeeringDB respectively

```bash
python3 traceroute_fetch.py
python3 ixp_info.py
python3 asn_fac.py
```
# The first script is going to create 2 files, the first one is a dictionary type file which contains all the useful data in the same format as in the traceroute file, and the second one is the directed graph containing all connections seen in the traceroute file.
# "ixp_info.py" only has one output and contains a dictionary with all the IXPs and their corresponding useful peering data.
# "asn_fac.py" provides a mapping between the ASNs and facilities they are present at.

## License

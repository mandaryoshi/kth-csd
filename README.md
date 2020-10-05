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
```

## License

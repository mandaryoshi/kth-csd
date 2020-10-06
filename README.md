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
* The first script is going to create 2 files, the first one ("traceroute_results.json") is a dictionary type file which contains all the useful data in the same format as in the traceroute file, and the second one ("traceroute_graph.gpickle") is the directed graph containing all connections seen in the traceroute file.
* "ixp_info.py" only has one output ("ixp_info_results.json") and contains a dictionary with all the IXPs and their corresponding useful peering data.
* "asn_fac.py" provides a mapping between the ASNs and the facilities they are present at. ("asn_fac_results.json")


Once the scripts that retrieve the information from the databases are done we get into phase 1 scrips which use this data to retrieve and classify the information.

* Script A: this script is used as part of other scripts to check if insisde an array of IP adresses (extracted from a traceroute) a IXP adress exists, returning the ID and IP of that IXP IP. To test the script individually you can run a simple script in which you create an instance of the IxpDetector class, and execute the detection method inserting an array of IPs as parameter for the function, then you can print the results.

* Script B: Works in a similar way as "script A", but in this case the input array it's supposed to be an array of IXP IPs and the result will be the ASN matched with each IP.

* Script C: The structure used in c is the same as a) and b) but in this case we thought that the input would be more useful in phase 2 if the input was only on IXP IP as when we analyze the traceroutes it will be done one by one to infer the facilities so there will be only 1 IP, and the result in this case is an array containing the Facilities where that IXP is present.

* Script D: ----

* Script E: To use this script just run it like a normal python3 script, like in the first step, this will output a file called "hop_results" where you will find the previous and next hops to all IXP IP hops in a traceroute file, with the consideration that only one IXP hop will be found in each (note: there's some cases where 2 IXP IPs can be found consecutively)

* Script F: In this script we make use of a class structure again, and this time the input for the function is a IP hop, which should be extracted from script e) and the return will be an array of neighbours of the hop, found in the graph previously created in the first step.

## License

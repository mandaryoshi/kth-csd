# Identifying Network Disruptions Affecting Colocation Facilities

We use the RIPE Atlas platform to monitor peering interconnections established over IXP links that assist the traffic exchange of networks in colocation data centers.  We analyze traceroute measurements performed on an Internet wide scale, build an anomaly detection tool that monitors the public peering links we identify, and report cases where the signal we extracted deviates from normal.

## Installation

Use the following 

```bash
pip install tqdm
pip install pytricia
pip install ujson
pip install networkx
pip install matplotlib
pip install numpy
```

## Usage Part 1

First run these scripts to get ixp info and facility info from PeeringDB and CAIDA respectively.

```bash
python3 ixp_info.py
python3 asn_fac.py
python3 fac_loc.py
python3 nonixp_info.py
```

* "ixp_info.py" only has one output ("ixp_info_results.json") and contains a dictionary with all the IXPs and their corresponding useful peering data.
* "asn_fac.py" provides a mapping between the ASNs and the facilities they are present at. ("asn_fac_results.json")
* "fac_loc.py" provides the coordinates, name and city of all colocation facilities in PeeringDB
* "nonixp_info.py" provides a mapping between the IP prefix and ASN from the CAIDA data-set stored as a dictionary, which is then parsed by the 'Pytricia' python library.

Then, by running "daily_analysis.sh", with the inputs of "start date" and "end date", traceroute information from RIPE Atlas is downloaded, extracted and organised into folders. This traceroute data is then analysed by script "scripte.py", and IXP hops are found. Lastly, "fw_model.py" is run to obtain colocation facilities observed in hourly traceroute dumps using Script A, Script B, Script C, Script D, Script F and phase2_impl.py.

* Script A: this script is used as part of other scripts to check if insisde an array of IP adresses (extracted from a traceroute) a IXP address exists, returning the ID and IP of that IXP IP. To test the script individually you can run a simple script in which you create an instance of the IxpDetector class, and execute the detection method inserting an array of IPs as parameter for the function, then you can print the results.

* Script B: Works in a similar way as "script A", but in this case the input array it's supposed to be an array of IXP IPs and the result will be the ASN matched with each IP.

* Script C: The structure used in c is the same as a) and b) but in this case we thought that the input would be more useful in phase 2 if the input was only on IXP IP as when we analyze the traceroutes it will be done one by one to infer the facilities so there will be only 1 IP, and the result in this case is an array containing the Facilities where that IXP is present.

* Script D: This script takes a single non-IXP IP as its input and returns the ASN of the same. The mapping is retrieved from the 'nonixp_info_results.json' file. 

* Script E: To use this script just run it like a normal python3 script, like in the first step, this will output a file called "hop_results" where you will find the previous and next hops to all IXP IP hops in a traceroute file, with the consideration that only one IXP hop will be found in each (note: there's some cases where 2 IXP IPs can be found consecutively)

* Script F: In this script we make use of a class structure again, and this time the input for the function is a IP hop, which should be extracted from script e) and the return will be an array of neighbours of the hop, found in the graph previously created in the first step.

* phase2_impl.py: This is the main script which is tasked with conducting the Constrained Facility Search (CFS) methodology, and is able to obtain both near-end and far-end facilities using the results from scripte.py which is the hop_results. The hop_results consists of the IXP hop, its previous hop and the next hop. 

## Usage Part 2

After the initial results have been obtained, these can now be analysed. To do so, there are two methods that can be used - the forwarding model and the rtt monitoring. 

* Forwarding model

To obtain results from the forwarding model, run the following in order: fw_monitoring.sh which consists of fw_initial_ref.py and fw_link_monitoring.py to calculate the initial and hourly values. Once this is complete, one can run fw_alarms which runs fw_alarm_references.py every 7 days and fw_alarm_monitoring.py for every hour. 

Once this is done, one can run the fw_deviations.py to see links and their anomalous values in one graph. The script which generates the graphs is named fw_patterns_graph.py, and is modifiable to display the number of probes, along with the reference values, red alarms and yellow alarms. 

* RTT monitoring

For the RTT monitoring, one has to run rtt_monitoring.sh which runs rtt_initial_ref.py and rtt_link_monitoring.py to calculate the reference values and compare these to the observed values for each hour. 

Once complete, the results can be seen by running rtt_monitoring_graph.py. 

* Statistics

Regarding statistics about both the forwarding model and rtt monitoring, scripts rtt_alarm_stats.py and fw_alarm_stats.py can be run. 
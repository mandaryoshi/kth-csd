#!/bin/bash

echo "INSERT DATE (YYYY-MM-DD):"
read date
echo "INSERT HOUR (HHMM):"
read hour 

echo "CREATING FOLDERS"

mkdir /home/csd/traceroutes/$date
mkdir /home/csd/traceroutes/$date/$hour

echo "DOWNLOADING TRACEROUTES FILE"

wget https://data-store.ripe.net/datasets/atlas-daily-dumps/$date/traceroute-$date\T$hour.bz2 -P /home/csd/traceroutes/$date/$hour/

echo "FILE DOWNLOADED"

echo "DECOMPRESSING FILE"

bzip2 -d /home/csd/traceroutes/$date/$hour/traceroute-$date\T$hour.bz2

echo "FILE DECOMPRESSED"

echo "FILTERING TRACEROUTES"

python3 traceroute_fetch.py $date $hour

echo "TRACEROUTES SUCCESSFULLY FILTERED"

rm /home/csd/traceroutes/$date/$hour/traceroute-$date\T$hour.bz2
rm /home/csd/traceroutes/$date/$hour/traceroute-$date\T$hour

echo "LOOKING FOR IXP HOPS"

python3 phase1_scripts/scripte.py $date $hour 

echo "IXP HOPS FOUND"

echo "FORWARDING MODEL ONGOING"

python3 phase3_scripts/fw_model.py $date $hour

rm /home/csd/traceroutes/$date/$hour/traceroute_results

echo "CONSTRAINT FACILITY SEARCH PERFORMED SUCCESSFULLY"

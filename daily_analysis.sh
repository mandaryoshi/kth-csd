#!/bin/bash

echo "INSERT DATE (YYYY-MM-DD):"
read date

mkdir /home/csd/traceroutes/$date

for hour in {00..23}

do

echo "CREATING FOLDERS"

mkdir /home/csd/traceroutes/$date/$hour\00

echo "DOWNLOADING TRACEROUTES FILE"

wget https://data-store.ripe.net/datasets/atlas-daily-dumps/$date/traceroute-$date\T$hour\00.bz2 -P /home/csd/traceroutes/$date/$hour\00/

echo "FILE DOWNLOADED"

echo "DECOMPRESSING FILE"

bzip2 -d /home/csd/traceroutes/$date/$hour\00/traceroute-$date\T$hour\00.bz2

echo "FILE DECOMPRESSED"

echo "FILTERING TRACEROUTES"

python3 traceroute_fetch.py $date $hour\00

echo "TRACEROUTES SUCCESSFULLY FILTERED"

rm /home/csd/traceroutes/$date/$hour\00/traceroute-$date\T$hour\00.bz2
rm /home/csd/traceroutes/$date/$hour\00/traceroute-$date\T$hour\00

echo "LOOKING FOR IXP HOPS"

python3 phase1_scripts/scripte.py $date $hour\00

echo "IXP HOPS FOUND"

echo "FORWARDING MODEL ONGOING"

python3 phase3_scripts/fw_model/fw_model.py $date $hour\00

rm /home/csd/traceroutes/$date/$hour\00/traceroute_results

echo "CONSTRAINT FACILITY SEARCH PERFORMED SUCCESSFULLY"

done

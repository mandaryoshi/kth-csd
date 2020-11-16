#!/bin/bash

echo "INSERT START DATE (YYYY-MM-DD):"
read sdate
echo "INSERT END DATE (YYYY-MM-DD):"
read edate

startdate=$(date -I -d "$sdate") || exit -1
enddate=$(date -I -d "$edate")   || exit -1

date="$startdate"
while [ "$date" != "$enddate" ]; do

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

date=$(date -I -d "$date + 1 day")

done
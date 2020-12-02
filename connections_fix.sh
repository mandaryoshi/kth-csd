#!/bin/bash

echo "INSERT START DATE (YYYY-MM-DD):"
read sdate
echo "INSERT END DATE (YYYY-MM-DD):"
read edate

startdate=$(date -I -d "$sdate") || exit -1
enddate=$(date -I -d "$edate")   || exit -1

date="$startdate"
while [ "$date" != "$enddate" ]; do

for hour in {00..23}

do

echo "FORWARDING MODEL ONGOING " + $date + $hour

python3 phase3_scripts/fw_model/fw_model.py $date $hour\00

echo "CONSTRAINT FACILITY SEARCH PERFORMED SUCCESSFULLY"

done

echo "FINISHED DATE: " + $date

date=$(date -I -d "$date + 1 day")

done

# dates=('2020-11-07')
# for date in "${dates[@]}"
# do
#     echo "date is $date"
#     for hour in {00..23}
#     do
#         echo "hour is $hour"
#         python3 phase3_scripts/fw_model/fw_model.py $date $hour\00
#     done
# done
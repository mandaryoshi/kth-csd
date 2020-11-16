#!/bin/bash

read start_date
read end_date

startdate=$(date -I -d "$start_date") || exit -1
enddate=$(date -I -d "$end_date")     || exit -1

d="$startdate"
while [ "$d" != "$enddate" ]; do 
  

    for hour in {00..23}
    do
        #if [ "$d" == "$startdate" ] && [ $hour -le 03 ]
        #then
        #    :
        #else
        #    python3 fw_initial_ref.py $d $hour
        #    python3 fw_link_monitoring.py $d $hour
        #fi
        python3 fw_initial_ref.py $d $hour
        python3 fw_link_monitoring.py $d $hour
    done

    d=$(date -I -d "$d + 1 day")
done

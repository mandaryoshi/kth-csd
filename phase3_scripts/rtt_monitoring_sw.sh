#!/bin/bash

#for now, start with 2020-10-28 until the 2020-11-01

read start_date  #%yy/mm/dd
read curr_hour   #%hh
read end_date

python3 rtt_initial_ref_sw.py $start_date $curr_hour


startdate=$(date -I -d "$start_date") || exit -1
print(start_date)
enddate=$(date -I -d "$end_date")     || exit -1

#d="$startdate"
while [ "$startdate" != "$enddate" ]; do 
  

    for hour in {00..23}
    do
       python3 rtt_link_monitoring.py $startdate $hour\00
    done



    startdate=$(date -I -d "$startdate + 1 day")
done

#python3 rtt_monitoring_graph.py $start_date $end_date 58 60

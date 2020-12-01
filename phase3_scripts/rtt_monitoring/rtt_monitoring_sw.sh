#!/bin/bash

#for now, start with 2020-10-28 until the 2020-11-01

read -p "Enter Start Date (yyyy-mm-dd):" start_date 
read -p "Enter End Date (yyyy-mm-dd):" end_date
read -p "Enter normal reference split:" ref_split 
read -p "Enter threshold method to detect alarm ( First for 1ms or Second for New method):" threshold

startdate=$(date -I -d "$start_date") || exit -1
enddate=$(date -I -d "$end_date")     || exit -1
if [ "$threshold" == "First" ];then
    file1="rtt_initial_ref_sw.py"
    file2="rtt_link_monitoring_sw.py"
elif [ "$threshold" ==  "Second" ];then
    file1="rtt_initial_ref_sw_bk.py"
    file2="rtt_link_monitoring_sw_bk.py"
fi

while [ "$startdate" != "$enddate" ]; do 
  
    echo $startdate
    for hour in {00..23}
    do
       python3 $file1 $startdate $hour $ref_split
       python3 $file2 $startdate $hour\00
    done

    startdate=$(date -I -d "$startdate + 1 day")
done

#python3 rtt_monitoring_graph.py $start_date $end_date 58 60

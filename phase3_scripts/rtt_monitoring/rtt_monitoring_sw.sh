#!/bin/bash
#This script computes initial references for rtts(based on 24hrs prior to current hr) for all hrs between start date and end date. 
#It also compares current hr rtt measurements to initial reference and raises alarm for any anomaly found.

read -p "Enter Start Date (yyyy-mm-dd):" start_date 
read -p "Enter End Date (yyyy-mm-dd):" end_date
read -p "Enter normal reference split value :" ref_split 
read -p "Enter A for 1ms threshold or B for optimized threshold):" threshold

startdate=$(date -I -d "$start_date") || exit -1
enddate=$(date -I -d "$end_date")     || exit -1
if [ "$threshold" == "A" ];then
    file1="rtt_initial_ref_sw.py"
    file2="rtt_link_monitoring_sw.py"
elif [ "$threshold" ==  "B" ];then
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

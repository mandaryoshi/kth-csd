#!/bin/bash
#This script computes initial references for rtts(based on 24hrs prior to current hr) for all hrs between start date and end date. 
#It also compares current hr rtt measurements to initial reference and raises alarm for any anomaly found.
for i in {1..3}
    do
        echo '**********************************************************'
    done
echo '************* RTT DELAY MONITORING ***********************'
for i in {1..3}
    do
        echo '**********************************************************'
    done
echo ''
read -p "Enter Start Date (yyyy-mm-dd):" start_date 
echo ''
read -p "Enter End Date (yyyy-mm-dd):" end_date
echo ''
read -p "Enter normal reference split value :" ref_split 
echo ''

startdate=$(date -I -d "$start_date") || exit -1
enddate=$(date -I -d "$end_date")     || exit -1
file1="rtt_initial_ref.py"
file2="rtt_link_monitoring.py"

while [ "$startdate" != "$enddate" ]; do 
  
    echo '********** Date: '$startdate' **********'
    for hour in {00..23}
    do
       python3 $file1 $startdate $hour $ref_split
       python3 $file2 $startdate $hour\00
    done

    startdate=$(date -I -d "$startdate + 1 day")
done

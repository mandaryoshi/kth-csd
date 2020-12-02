#!/bin/bash

read start_date
read end_date

startdate=$(date -I -d "$start_date") || exit -1
enddate=$(date -I -d "$end_date")     || exit -1

d="$startdate"

i=0
monitor=false
while [ "$d" != "$enddate" ]; do 
    
    if [ $i -ge 7 ];
    then
        monitor=true
        python3 fw_alarm_references.py $d
        i=0
    fi
    
    
    for hour in {00..23}
    do
        if [ $monitor = true ];
        then
            python3 fw_alarm_monitoring.py $d $hour
        fi
    done
    
    let "i+=1"
    d=$(date -I -d "$d + 1 day")
done
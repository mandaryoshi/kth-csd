#!/bin/bash

for i in {1..3}
    do
        echo '**********************************************************'
    done
echo '************* FORWARDING MODEL MONITORING ****************'

for i in {1..3}
    do
        echo '**********************************************************'
    done

echo "INSERT START DATE (YYYY-MM-DD):"
read start_date
echo "INSERT END DATE (YYYY-MM-DD):"
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

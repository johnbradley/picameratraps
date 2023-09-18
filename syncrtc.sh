#!/bin/bash
echo "Syncing RTC from system clock"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    ssh pi@$HOST sudo hwclock -w --verbose
done

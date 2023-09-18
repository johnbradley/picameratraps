#!/bin/bash
ALARM=$1
ARGHOST=$2
echo "Running hibernate for $ALARM on camera traps"
for HOST in $(./traplist.sh $ARGHOST)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    ssh pi@$HOST ./scripts/hibernate.sh $ALARM
done

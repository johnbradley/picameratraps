#!/bin/bash
echo "Checking camera trap status"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    ssh pi@$HOST -o ConnectTimeout=4  ./scripts/status.sh
done

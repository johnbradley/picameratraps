#!/bin/bash
echo "Disabling bluetooth"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    ssh pi@$HOST -o ConnectTimeout=4  ./scripts/disablebt.sh
done
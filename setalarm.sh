#!/bin/bash
echo "Setting up camera traps"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    echo "Sync remote-files to $HOST"
    rsync --recursive --perms remote-files/* pi@$HOST:.
    echo "Running 'python ./scripts/capture.py init' on $HOST"
    ssh pi@$HOST python ./scripts/capture.py init
done

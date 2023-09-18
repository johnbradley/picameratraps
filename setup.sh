#!/bin/bash
echo "Setting up camera traps"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    echo "Sync remote-files to $HOST"
    rsync --recursive --perms remote-files/* pi@$HOST:.
    echo "Running ./scripts/setup.sh on $HOST"
    ssh pi@$HOST ./scripts/setup.sh
done
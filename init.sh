#!/bin/bash
echo "Perform one-time setup on camera traps"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    echo "Sync remote-files to $HOST"
    rsync --recursive --perms remote-files/* pi@$HOST:.
    echo "Running ./scripts/init.sh on $HOST"
    ssh pi@$HOST ./scripts/init.sh
done
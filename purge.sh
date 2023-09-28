#!/bin/bash
echo "Deleting images from camera traps older than 24 hours"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    ssh pi@$HOST find images/ -type f -mtime +0 -delete
    ssh pi@$HOST find videos/ -type f -mtime +0 -delete
done

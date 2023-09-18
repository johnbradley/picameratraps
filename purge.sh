#!/bin/bash
echo "Deleting images from camera traps older than 1 day"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    ssh pi@$HOST find images/ -type f -mtime +1 -delete

done
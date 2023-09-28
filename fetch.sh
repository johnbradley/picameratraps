#!/bin/bash
echo "Fetching images from camera traps"
for HOST in $(./traplist.sh $1)
do
    echo "----------------------"
    echo "$HOST"
    echo "----------------------"
    mkdir -p results/$HOST
    rsync -v --stats --progress --recursive --times pi@$HOST:images results/$HOST
    rsync -v --stats --progress --recursive --times pi@$HOST:videos results/$HOST
done

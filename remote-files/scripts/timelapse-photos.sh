#!/bin/bash
# record an image every minute for an hour
set -e
TIMELAPSE_SEC=$1
TIMEOUT_SEC=$2
TIMEOUT_MS=$((TIMEOUT_SEC * 1000))
TIMELAPSE_MS=$((TIMELAPSE_SEC * 1000))
echo "Recording an image every ${TIMEOUT_SEC} seconds for ${TIMELAPSE_SEC}" >> logs/record.log
echo "Waiting for start of the minute"
./scripts/sleep-until-minute-start.sh
cd images
libcamera-still --timeout ${TIMEOUT_MS} --timelapse ${TIMELAPSE_MS} --datetime --nopreview  >> ../logs/record.log 2>&1

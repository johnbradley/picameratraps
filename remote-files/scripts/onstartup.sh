#!/bin/bash
cd /home/pi
LOG=./logs/onstart.log
touch $LOG
echo "Starting up " >> $LOG
date >> $LOG
python ./scripts/capture.py >> $LOG 2>&1

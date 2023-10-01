#!/bin/bash
cd /home/pi
LOG=./logs/onstart.log
touch $LOG
echo "Starting up " >> $LOG
date >> $LOG
python ./scripts/onstartup.py >> $LOG 2>&1

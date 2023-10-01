#!/bin/bash
set -e
echo "Running sleep $1" >> logs/sleep.log
date  >> logs/sleep.log
python ./scripts/setalarm.py $1  >> logs/sleep.log
./scripts/shutdown.sh
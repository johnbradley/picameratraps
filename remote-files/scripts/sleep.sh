#!/bin/bash
set -e
python ./scripts/setalarm.py $1
./scripts/shutdown.sh
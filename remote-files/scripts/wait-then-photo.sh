#!/bin/bash
./scripts/sleep-until-minute-start.sh
cd images
libcamera-still --datetime --nopreview >> ../logs/record.log 2>&1

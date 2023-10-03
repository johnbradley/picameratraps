#!/bin/bash
RECORD_TIME_MS=$1
PREFIX=$2
libcamera-vid -t ${RECORD_TIME_MS} -o videos/${PREFIX}.h264 --save-pts videos/${PREFIX}.ts.txt --nopreview >> logs/record.log 2>&1
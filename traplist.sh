#!/bin/bash
HOST=$1
if [[ -z "${HOST}" ]]
then
  cat cameratraps.txt
else
  echo $HOST
fi

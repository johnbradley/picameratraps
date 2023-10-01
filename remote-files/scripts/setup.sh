#!/bin/bash
set -e

echo "Creating images/ directory"
mkdir -p images

echo "Creating videos/ directory"
mkdir -p videos

echo "Setting up cron"
crontab crontab.txt

echo "Setting up cameratrap.serivce to run onstartup.sh"
DEST=/lib/systemd/system/cameratrap.service
sudo cp cameratrap.service $DEST
sudo chmod 644 $DEST
sudo systemctl daemon-reload
sudo systemctl enable cameratrap.service

#!/bin/bash
set -e

echo "Creating images/ directory"
mkdir -p images

echo "Creating videos/ directory"
mkdir -p videos

echo "Setting up cron"
crontab crontab.txt

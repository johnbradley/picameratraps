#!/bin/bash
set -e

echo "Setting up cron"
crontab crontab.txt

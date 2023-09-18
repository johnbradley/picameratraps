#!/bin/bash
HOST=$1
echo "Video streaming for $HOST"

echo "Open another terminal and run:"
echo "vlc tcp/h264://$HOST:8888/"
echo "Press Ctrl-C to terminte the video streaming"
ssh pi@$HOST ./scripts/streamvid.sh
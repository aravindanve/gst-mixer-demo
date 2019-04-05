#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

VIDEO_RTP_ENCODING_NAME=VP8 \
  ${SCRIPTPATH}/../factory/packager_test.py &

while true; do
  echo "(re)starting source..."
  (${SCRIPTPATH}/srcs/rtpsrc_3000_vp8+opus.sh > /dev/null 2>&1) & pid=$!

  sleep 10

  echo "killing src..."
  # NOTE: kill subshell processes and their gst child processes
  pkill -2 -P $pid
done

wait

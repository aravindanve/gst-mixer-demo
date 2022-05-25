#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

DEBUG_INPUT=true \
VIDEO_RTP_ENCODING_NAME=VP8 \
  ${SCRIPTPATH}/../factory/packager_test.py &

# test restart
for i in 0 1 2; do
  echo "(re)starting source..."
  (${SCRIPTPATH}/srcs/rtpsrc_3000_vp8+opus.sh > /dev/null 2>&1) & pid=$!

  sleep 5

  echo "killing src..."
  # NOTE: kill subshell processes and their gst child processes
  pkill -2 -P $pid
done

# test timeout
while true; do
  echo "(re)starting source..."
  (${SCRIPTPATH}/srcs/rtpsrc_3000_vp8+opus.sh > /dev/null 2>&1) & pid=$!

  sleep 5

  echo "killing src..."
  # NOTE: kill subshell processes and their gst child processes
  pkill -2 -P $pid

  sleep 60
done

wait

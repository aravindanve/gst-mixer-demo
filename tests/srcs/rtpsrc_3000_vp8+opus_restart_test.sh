#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

while true; do
  echo "(re)starting source..."
  (${SCRIPTPATH}/rtpsrc_3000_vp8+opus.sh > /dev/null 2>&1) & src_pid=$!

  echo "(re)starting sink..."
  (${SCRIPTPATH}/../sinks/rtpsink_3000_vp8+opus.sh > /dev/null 2>&1) & sink_pid=$!

  sleep 10

  echo "killing src and sink..."
  # NOTE: kill subshell processes and their gst child processes
  pkill -2 -P $src_pid
  pkill -2 -P $sink_pid
done

wait

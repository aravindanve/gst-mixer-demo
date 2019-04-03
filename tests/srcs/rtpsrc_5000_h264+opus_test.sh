#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

${SCRIPTPATH}/rtpsrc_5000_h264+opus.sh &
${SCRIPTPATH}/../sinks/rtpsink_5000_h264+opus.sh &

wait

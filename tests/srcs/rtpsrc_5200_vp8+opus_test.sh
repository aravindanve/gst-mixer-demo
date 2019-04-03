#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

${SCRIPTPATH}/rtpsrc_5200_vp8+opus.sh &
${SCRIPTPATH}/../sinks/rtpsink_5200_vp8+opus.sh &

wait

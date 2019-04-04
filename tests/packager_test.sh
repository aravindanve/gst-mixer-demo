#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

# ${SCRIPTPATH}/srcs/rtpsrc_3000_h264+opus.sh > /dev/null 2>&1 &
${SCRIPTPATH}/../factory/packager_test.py &

wait

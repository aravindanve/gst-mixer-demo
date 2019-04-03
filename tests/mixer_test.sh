#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

${SCRIPTPATH}/srcs/rtpsrc_5000_vp8+opus.sh > /dev/null 2>&1 &
${SCRIPTPATH}/srcs/rtpsrc_5100_vp8+opus.sh > /dev/null 2>&1 &
${SCRIPTPATH}/../factory/mixer_test.py &

wait

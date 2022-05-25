#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

DEBUG_OUTPUT=true \
VIDEO_RTP_ENCODING_NAME=H264 \
  ${SCRIPTPATH}/../factory/packager_test.py &

${SCRIPTPATH}/srcs/rtpsrc_3000_h264+opus.sh > /dev/null 2>&1

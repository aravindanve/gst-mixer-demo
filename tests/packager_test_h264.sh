#!/bin/bash

SCRIPTPATH=$(dirname "$0")

trap killgroup SIGINT

killgroup() {
  echo "Received SIGINT..."
  kill 0
}

VIDEO_RTP_ENCODING_NAME=H264 \
  ${SCRIPTPATH}/../factory/packager_test.py &

while true; do
echo "Starting src...."
${SCRIPTPATH}/srcs/rtpsrc_3000_h264+opus.sh > /dev/null 2>&1 &
pid=$!
sleep 10

echo "Killing src...."
kill -2 $pid
done

wait
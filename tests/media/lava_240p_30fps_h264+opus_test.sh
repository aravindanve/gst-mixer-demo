#!/bin/bash

SCRIPTPATH=$(dirname "$0")

GST_DEBUG_DUMP_DOT_DIR=. \
gst-launch-1.0 filesrc location=${SCRIPTPATH}/lava_240p_30fps_h264+opus.mkv ! decodebin name=decoder \
    decoder. ! queue ! videoconvert ! autovideosink \
    decoder. ! queue ! audioconvert ! autoaudiosink

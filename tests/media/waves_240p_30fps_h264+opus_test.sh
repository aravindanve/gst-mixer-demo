#!/bin/bash

SCRIPTPATH=$(dirname "$0")

gst-launch-1.0 filesrc location=${SCRIPTPATH}/montreal_240p_30fps_h264+opus.mkv ! decodebin name=decoder \
    decoder. ! queue ! videoconvert ! autovideosink \
    decoder. ! queue ! audioconvert ! autoaudiosink

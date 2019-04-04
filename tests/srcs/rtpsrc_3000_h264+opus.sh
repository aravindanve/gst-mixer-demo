#!/bin/bash

SCRIPTPATH=$(dirname "$0")

gst-launch-1.0 -v \
    rtpbin name=rtpbin \
    rtpbin.send_rtp_src_0 \
    ! udpsink host=127.0.0.1 port=3000 \
    rtpbin.send_rtcp_src_0 \
    ! udpsink host=127.0.0.1 port=3001 sync=false async=false \
    udpsrc address=127.0.0.1 port=4000 \
    ! rtpbin.recv_rtcp_sink_0 \
    rtpbin.send_rtp_src_1 \
    ! udpsink host=127.0.0.1 port=3002 \
    rtpbin.send_rtcp_src_1 \
    ! udpsink host=127.0.0.1 port=3003 sync=false async=false \
    udpsrc address=127.0.0.1 port=4002 \
    ! rtpbin.recv_rtcp_sink_1 \
    multiqueue name=multiq \
    multifilesrc \
        loop=true \
        location=${SCRIPTPATH}/../media/lava_240p_30fps_h264+opus.mkv \
    ! matroskademux name=demux \
    demux. \
    ! video/x-h264,width=426,height=240,framerate=30/1,profile=high,interlace-mode=mixed \
    ! multiq.sink_0 \
    demux. \
    ! audio/x-opus,rate=48000,channels=2,channel-mapping-family=0,stream-count=1,coupled-count=1 \
    ! multiq.sink_1 \
    multiq.src_0 \
    ! queue \
    ! rtph264pay \
        config-interval=1 \
    ! application/x-rtp,clock-rate=90000,payload=101 \
    ! rtpbin.send_rtp_sink_0 \
    multiq.src_1 \
    ! queue \
    ! rtpopuspay \
    ! application/x-rtp,clock-rate=48000,payload=100 \
    ! rtpbin.send_rtp_sink_1

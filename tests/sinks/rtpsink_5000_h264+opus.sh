#!/bin/bash

SCRIPTPATH=$(dirname "$0")

gst-launch-1.0 -v \
    rtpbin name=rtpbin \
    udpsrc \
        caps="application/x-rtp,media=video,clock-rate=90000,encoding-name=H264,payload=101" \
        port=5000 \
        address=127.0.0.1 \
    ! rtpbin.recv_rtp_sink_0 \
    udpsrc \
        port=5001 \
        address=127.0.0.1 \
    ! rtpbin.recv_rtcp_sink_0 \
    rtpbin.send_rtcp_src_0 \
    ! udpsink port=6000 \
        sync=false \
        async=false \
    rtpbin. \
    ! rtph264depay \
    ! h264parse \
    ! avdec_h264 \
    ! videoconvert \
    ! autovideosink \
    udpsrc \
        caps="application/x-rtp,media=audio,clock-rate=48000,encoding-name=OPUS,payload=100" \
        port=5002 \
        address=127.0.0.1 \
    ! rtpbin.recv_rtp_sink_1 \
    udpsrc \
        port=5003 \
        address=127.0.0.1 \
    ! rtpbin.recv_rtcp_sink_1 \
    rtpbin.send_rtcp_src_1 \
    ! udpsink port=6001 \
        sync=false \
        async=false \
    rtpbin. \
    ! rtpopusdepay \
    ! opusdec \
    ! audioconvert \
    ! autoaudiosink

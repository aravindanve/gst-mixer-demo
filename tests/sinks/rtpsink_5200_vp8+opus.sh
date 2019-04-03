#!/bin/bash

SCRIPTPATH=$(dirname "$0")

gst-launch-1.0 -v \
    rtpbin name=rtpbin \
    udpsrc \
        caps="application/x-rtp,media=video,clock-rate=90000,encoding-name=VP8,payload=101" \
        port=5200 \
        address=127.0.0.1 \
    ! rtpbin.recv_rtp_sink_0 \
    udpsrc \
        port=5201 \
        address=127.0.0.1 \
    ! rtpbin.recv_rtcp_sink_0 \
    rtpbin.send_rtcp_src_0 \
    ! udpsink port=6200 \
        sync=false \
        async=false \
    rtpbin. \
    ! rtpvp8depay \
    ! vp8dec \
    ! videoconvert \
    ! autovideosink \
    udpsrc \
        caps="application/x-rtp,media=audio,clock-rate=48000,encoding-name=OPUS,payload=100" \
        port=5202 \
        address=127.0.0.1 \
    ! rtpbin.recv_rtp_sink_1 \
    udpsrc \
        port=5203 \
        address=127.0.0.1 \
    ! rtpbin.recv_rtcp_sink_1 \
    rtpbin.send_rtcp_src_1 \
    ! udpsink port=6201 \
        sync=false \
        async=false \
    rtpbin. \
    ! rtpopusdepay \
    ! opusdec \
    ! audioconvert \
    ! autoaudiosink

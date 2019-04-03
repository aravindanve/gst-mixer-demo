ffmpeg -i montreal.mp4 \
    -vf 'scale=-2:240' \
    -crf 23 \
    -preset fast \
    -codec:a libopus \
    -ar 48000 \
    -b:a 96k \
    -codec:v libx264 \
    -profile:v high \
    -level 4.2 \
    -r 30 \
    -b:v 400k \
    -maxrate 700k \
    -bufsize 1400k \
    montreal_240p_30fps_h264+opus.mkv

ffmpeg -i montreal.mp4 \
    -vf 'scale=-2:240' \
    -crf 8 \
    -codec:a libopus \
    -ar 48000 \
    -b:a 96k \
    -codec:v libvpx \
    -r 30 \
    -b:v 400k \
    -maxrate 700k \
    -bufsize 1400k \
    montreal_240p_30fps_vp8+opus.mkv

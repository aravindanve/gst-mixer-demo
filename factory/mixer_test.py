#!/usr/bin/env python3

import gi; gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from threading import Timer

from mixer import *

if __name__ == '__main__':
    set_log_level(LogLevel.ALL)

    Gst.init(None)
    Gst.debug_set_active(True)
    Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

    loop = GLib.MainLoop()
    refs = {}

    def do_action(name, action, *ref_names, **kwargs):
        global refs

        log_info('%s = %s(%s)' % (name, action.__name__, ','.join(ref_names)))

        args = [refs[ref_name] for ref_name in ref_names]
        refs[name] = action(*args, **kwargs)

    Timer(0, do_action, args=['mixer', do_mixer_init], kwargs={
        'debug': True,
        'debug_output': True,
        'default_pattern': 'snow',
        'default_wave': 'red-noise',
        'video_width': 426,
        'video_height': 240,
        'video_local_port': 4000,
        'video_remote_port': 3000,
        'audio_local_port': 4002,
        'audio_remote_port': 3001 }).start()

    Timer(2, do_action, args=[None, do_mixer_start, 'mixer']).start()

    Timer(4, do_action, args=['stream_0', do_mixer_stream_init, 'mixer'], kwargs={
        'media': 'video',
        'clock_rate': 90000,
        'encoding_name': 'VP8',
        'payload': 101,
        'local_port': 5000,
        'remote_port': 6000 }).start()

    Timer(4, do_action, args=['stream_1', do_mixer_stream_init, 'mixer'], kwargs={
        'media': 'audio',
        'clock_rate': 48000,
        'encoding_name': 'OPUS',
        'payload': 100,
        'local_port': 5002,
        'remote_port': 6001 }).start()

    Timer(10, do_action, args=['stream_0', do_mixer_stream_dispose, 'mixer', 'stream_0']).start()
    Timer(10, do_action, args=['stream_1', do_mixer_stream_dispose, 'mixer', 'stream_1']).start()

    Timer(15, do_action, args=['stream_2', do_mixer_stream_init, 'mixer'], kwargs={
        'media': 'video',
        'clock_rate': 90000,
        'encoding_name': 'VP8',
        'payload': 101,
        'local_port': 5100,
        'remote_port': 6100 }).start()

    Timer(15, do_action, args=['stream_3', do_mixer_stream_init, 'mixer'], kwargs={
        'media': 'audio',
        'clock_rate': 48000,
        'encoding_name': 'OPUS',
        'payload': 100,
        'local_port': 5102,
        'remote_port': 6101 }).start()

    Timer(25, do_action, args=['stream_2', do_mixer_stream_dispose, 'mixer', 'stream_2']).start()
    Timer(25, do_action, args=['stream_3', do_mixer_stream_dispose, 'mixer', 'stream_3']).start()

    Timer(30, do_action, args=['stream_0', do_mixer_stream_init, 'mixer'], kwargs={
        'media': 'video',
        'clock_rate': 90000,
        'encoding_name': 'VP8',
        'payload': 101,
        'local_port': 5000,
        'remote_port': 6000 }).start()

    Timer(30, do_action, args=['stream_1', do_mixer_stream_init, 'mixer'], kwargs={
        'media': 'audio',
        'clock_rate': 48000,
        'encoding_name': 'OPUS',
        'payload': 100,
        'local_port': 5002,
        'remote_port': 6001 }).start()

    Timer(40, do_action, args=['stream_2', do_mixer_stream_init, 'mixer'], kwargs={
        'media': 'video',
        'clock_rate': 90000,
        'encoding_name': 'VP8',
        'payload': 101,
        'local_port': 5100,
        'remote_port': 6100 }).start()

    Timer(40, do_action, args=['stream_3', do_mixer_stream_init, 'mixer'], kwargs={
        'media': 'audio',
        'clock_rate': 48000,
        'encoding_name': 'OPUS',
        'payload': 100,
        'local_port': 5102,
        'remote_port': 6101 }).start()

    Timer(50, do_action, args=['stream_0', do_mixer_stream_dispose, 'mixer', 'stream_0']).start()
    Timer(50, do_action, args=['stream_1', do_mixer_stream_dispose, 'mixer', 'stream_1']).start()
    Timer(60, do_action, args=['stream_2', do_mixer_stream_dispose, 'mixer', 'stream_2']).start()
    Timer(60, do_action, args=['stream_3', do_mixer_stream_dispose, 'mixer', 'stream_3']).start()
    Timer(70, do_action, args=['mixer', do_mixer_dispose, 'mixer']).start()
    Timer(75, loop.quit).start()

    loop.run()

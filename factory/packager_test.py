#!/usr/bin/env python3

import gi; gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from threading import Timer

from packager import *

if __name__ == '__main__':
    set_log_level(LogLevel.ALL)

    Gst.init(None)
    Gst.debug_set_active(True)
    Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

    loop = GLib.MainLoop()
    packager = do_packager_init(
        debug_output=True,
        default_pattern='snow',
        default_wave='red-noise',
        video_width=426,
        video_height=240,
        video_local_port=3000,
        video_remote_port=4000,
        audio_local_port=3002,
        audio_remote_port=4002)

    do_packager_start(packager)

    loop.run()

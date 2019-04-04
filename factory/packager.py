import gi; gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from threading import Lock

from shared import *
from logger import *

class Packager:
    pass

def do_packager_init(**kwargs):
    log_info(Packager, 'do_packager_init()')
    packager = Packager()

    packager.name = 'packager'
    packager.debug_output = kwargs.get('debug_output', False)

    packager.disposed = False
    packager.lock = Lock()

    packager.pipeline = Gst.Pipeline(packager.name)

    packager.video_rtp_clock_rate = kwargs.get('clock_rate') or 90000
    packager.video_rtp_encoding_name = kwargs.get('encoding_name') or 'VP8'
    packager.video_rtp_payload = kwargs.get('payload') or 101
    packager.audio_rtp_clock_rate = kwargs.get('clock_rate') or 48000
    packager.audio_rtp_encoding_name = kwargs.get('encoding_name') or 'OPUS'
    packager.audio_rtp_payload = kwargs.get('payload') or 100

    if packager.video_rtp_encoding_name not in ['VP8', 'H264']:
        log_error(packager, 'unsupported video encoding: %s' % packager.video_rtp_encoding_name)
        return

    if packager.audio_rtp_encoding_name not in ['OPUS']:
        log_error(packager, 'unsupported audio encoding: %s' % packager.audio_rtp_encoding_name)
        return

    packager.video_rtp_caps = Gst.caps_from_string(
        'application/x-rtp,media=video,clock-rate=%s,encoding-name=%s,payload=%s' % (
            packager.video_rtp_clock_rate, packager.video_rtp_encoding_name, packager.video_rtp_payload))

    packager.audio_rtp_caps = Gst.caps_from_string(
        'application/x-rtp,media=audio,clock-rate=%s,encoding-name=%s,payload=%s' % (
            packager.audio_rtp_clock_rate, packager.audio_rtp_encoding_name, packager.audio_rtp_payload))

    packager.rtp_bin = Gst.ElementFactory.make('rtpbin', 'rtp_bin')
    packager.rtp_bin.set_property('autoremove', True)
    packager.rtp_bin.set_property('drop-on-latency', True)
    packager.pipeline.add(packager.rtp_bin)

    packager.video_local_ip = kwargs.get('video_local_ip') or '127.0.0.1'
    packager.video_local_port = kwargs.get('video_local_port') or 3000
    packager.video_rtp_src = Gst.ElementFactory.make('udpsrc', '%s_video_rtp_src' % packager.name)
    packager.video_rtp_src.set_property('port', packager.video_local_port)
    packager.video_rtp_src.set_property('address', packager.video_local_ip)
    packager.video_rtp_src.set_property('caps', packager.video_rtp_caps)
    packager.pipeline.add(packager.video_rtp_src)

    video_rtp_src_srcpad = packager.video_rtp_src.get_static_pad('src')
    rtp_bin_rtp_sinkpad_0_template = packager.rtp_bin.get_pad_template('recv_rtp_sink_%u')
    rtp_bin_rtp_sinkpad_0 = packager.rtp_bin.request_pad(rtp_bin_rtp_sinkpad_0_template, 'recv_rtp_sink_0')
    video_rtp_src_srcpad.link(rtp_bin_rtp_sinkpad_0)

    packager.video_rtcp_src = Gst.ElementFactory.make('udpsrc', '%s_video_rtcp_src' % packager.name)
    packager.video_rtcp_src.set_property('port', packager.video_local_port + 1) # FIXME: use rtcp-mux
    packager.video_rtcp_src.set_property('address', packager.video_local_ip)
    packager.pipeline.add(packager.video_rtcp_src)

    video_rtcp_src_srcpad = packager.video_rtcp_src.get_static_pad('src')
    rtp_bin_rtcp_sinkpad_0_template = packager.rtp_bin.get_pad_template('recv_rtcp_sink_%u')
    rtp_bin_rtcp_sinkpad_0 = packager.rtp_bin.request_pad(rtp_bin_rtcp_sinkpad_0_template, 'recv_rtcp_sink_0')
    video_rtcp_src_srcpad.link(rtp_bin_rtcp_sinkpad_0)

    packager.video_remote_ip = kwargs.get('video_remote_ip') or '127.0.0.1'
    packager.video_remote_port = kwargs.get('video_remote_port') or 4001
    packager.video_rtcp_sink = Gst.ElementFactory.make('udpsink', '%s_video_rtcp_sink' % packager.name)
    packager.video_rtcp_sink.set_property('port', packager.video_remote_port)
    packager.video_rtcp_sink.set_property('host', packager.video_remote_ip)
    packager.video_rtcp_sink.set_property('async', False)
    packager.video_rtcp_sink.set_property('sync', False)
    packager.pipeline.add(packager.video_rtcp_sink)

    rtp_bin_rtcp_srcpad_0_template = packager.rtp_bin.get_pad_template('send_rtcp_src_%u')
    rtp_bin_rtcp_srcpad_0 = packager.rtp_bin.request_pad(rtp_bin_rtcp_srcpad_0_template, 'send_rtcp_src_0')
    video_rtcp_sink_sinkpad = packager.video_rtcp_sink.get_static_pad('sink')
    rtp_bin_rtcp_srcpad_0.link(video_rtcp_sink_sinkpad)

    packager.audio_local_ip = kwargs.get('audio_local_ip') or '127.0.0.1'
    packager.audio_local_port = kwargs.get('audio_local_port') or 3002
    packager.audio_rtp_src = Gst.ElementFactory.make('udpsrc', '%s_audio_rtp_src' % packager.name)
    packager.audio_rtp_src.set_property('port', packager.audio_local_port)
    packager.audio_rtp_src.set_property('address', packager.audio_local_ip)
    packager.audio_rtp_src.set_property('caps', packager.audio_rtp_caps)
    packager.pipeline.add(packager.audio_rtp_src)

    audio_rtp_src_srcpad = packager.audio_rtp_src.get_static_pad('src')
    rtp_bin_rtp_sinkpad_1_template = packager.rtp_bin.get_pad_template('recv_rtp_sink_%u')
    rtp_bin_rtp_sinkpad_1 = packager.rtp_bin.request_pad(rtp_bin_rtp_sinkpad_1_template, 'recv_rtp_sink_1')
    audio_rtp_src_srcpad.link(rtp_bin_rtp_sinkpad_1)

    packager.audio_rtcp_src = Gst.ElementFactory.make('udpsrc', '%s_audio_rtcp_src' % packager.name)
    packager.audio_rtcp_src.set_property('port', packager.audio_local_port + 1) # FIXME: use rtcp-mux
    packager.audio_rtcp_src.set_property('address', packager.audio_local_ip)
    packager.pipeline.add(packager.audio_rtcp_src)

    audio_rtcp_src_srcpad = packager.audio_rtcp_src.get_static_pad('src')
    rtp_bin_rtcp_sinkpad_1_template = packager.rtp_bin.get_pad_template('recv_rtcp_sink_%u')
    rtp_bin_rtcp_sinkpad_1 = packager.rtp_bin.request_pad(rtp_bin_rtcp_sinkpad_1_template, 'recv_rtcp_sink_1')
    audio_rtcp_src_srcpad.link(rtp_bin_rtcp_sinkpad_1)

    packager.audio_remote_ip = kwargs.get('audio_remote_ip') or '127.0.0.1'
    packager.audio_remote_port = kwargs.get('audio_remote_port') or 4003
    packager.audio_rtcp_sink = Gst.ElementFactory.make('udpsink', '%s_audio_rtcp_sink' % packager.name)
    packager.audio_rtcp_sink.set_property('port', packager.audio_remote_port)
    packager.audio_rtcp_sink.set_property('host', packager.audio_remote_ip)
    packager.audio_rtcp_sink.set_property('async', False)
    packager.audio_rtcp_sink.set_property('sync', False)
    packager.pipeline.add(packager.audio_rtcp_sink)

    rtp_bin_rtcp_srcpad_1_template = packager.rtp_bin.get_pad_template('send_rtcp_src_%u')
    rtp_bin_rtcp_srcpad_1 = packager.rtp_bin.request_pad(rtp_bin_rtcp_srcpad_1_template, 'send_rtcp_src_1')
    audio_rtcp_sink_sinkpad = packager.audio_rtcp_sink.get_static_pad('sink')
    rtp_bin_rtcp_srcpad_1.link(audio_rtcp_sink_sinkpad)

    packager.video_format = kwargs.get('video_format') or 'I420'
    packager.video_framerate = kwargs.get('video_framerate') or '30/1'
    packager.video_width = kwargs.get('video_width') or 1280
    packager.video_height = kwargs.get('video_height') or 720
    packager.video_caps = Gst.caps_from_string(
        'video/x-raw,format=%s,framerate=%s,width=%s,height=%s' % (
            packager.video_format, packager.video_framerate, packager.video_width, packager.video_height))

    packager.audio_format = kwargs.get('audio_format') or 'F32LE'
    packager.audio_rate = kwargs.get('audio_rate') or 44100
    packager.audio_channels = kwargs.get('audio_channels') or 2
    packager.audio_layout = kwargs.get('audio_layout') or 'interleaved'
    packager.audio_caps = Gst.caps_from_string(
        'audio/x-raw,format=%s,rate=%s,channels=%s,layout=%s' % (
            packager.audio_format, packager.audio_rate, packager.audio_channels, packager.audio_layout))

    default_pattern = kwargs.get('default_pattern') or 'black'
    packager.video_src = Gst.ElementFactory.make('videotestsrc', 'video_src')
    packager.video_src.set_property('is-live', True)
    packager.video_src.set_property('pattern', default_pattern)
    packager.pipeline.add(packager.video_src)

    packager.video_src_caps_filter = Gst.ElementFactory.make('capsfilter', 'video_src_caps_filter')
    packager.video_src_caps_filter.set_property('caps', packager.video_caps)
    packager.pipeline.add(packager.video_src_caps_filter)

    packager.video_src.link(packager.video_src_caps_filter)

    default_wave = kwargs.get('default_wave') or 'silence'
    default_volume = kwargs.get('default_volume') or 0.02
    packager.audio_src = Gst.ElementFactory.make('audiotestsrc', 'audio_src')
    packager.audio_src.set_property('is-live', True)
    packager.audio_src.set_property('wave', default_wave)
    packager.audio_src.set_property('volume', default_volume)
    packager.pipeline.add(packager.audio_src)

    packager.audio_src_caps_filter = Gst.ElementFactory.make('capsfilter', 'audio_src_caps_filter')
    packager.audio_src_caps_filter.set_property('caps', packager.audio_caps)
    packager.pipeline.add(packager.audio_src_caps_filter)

    packager.audio_src.link(packager.audio_src_caps_filter)

    packager.multi_queue = Gst.ElementFactory.make('multiqueue', 'multi_queue')
    packager.pipeline.add(packager.multi_queue)

    video_src_caps_filter_srcpad = packager.video_src_caps_filter.get_static_pad('src')
    multi_queue_sinkpad_0_template = packager.multi_queue.get_pad_template('sink_%u')
    multi_queue_sinkpad_0 = packager.multi_queue.request_pad(multi_queue_sinkpad_0_template , 'sink_0')
    video_src_caps_filter_srcpad.link(multi_queue_sinkpad_0)

    audio_src_caps_filter_srcpad = packager.audio_src_caps_filter.get_static_pad('src')
    multi_queue_sinkpad_1_template = packager.multi_queue.get_pad_template('sink_%u')
    multi_queue_sinkpad_1 = packager.multi_queue.request_pad(multi_queue_sinkpad_1_template , 'sink_1')
    audio_src_caps_filter_srcpad.link(multi_queue_sinkpad_1)

    if packager.video_rtp_encoding_name == 'H264':
        packager.video_depay = Gst.ElementFactory.make('rtph264depay', 'videodepay')
        packager.video_dec = Gst.ElementFactory.make('avdec_h264', 'video_dec')

    elif packager.video_rtp_encoding_name == 'VP8':
        packager.video_depay = Gst.ElementFactory.make('rtpvp8depay', 'videodepay')
        packager.video_dec = Gst.ElementFactory.make('vp8dec', 'dec')

    packager.pipeline.add(packager.video_depay)
    packager.pipeline.add(packager.video_dec)

    packager.video_rate = Gst.ElementFactory.make('videorate', 'video_rate')
    packager.pipeline.add(packager.video_rate)

    packager.video_convert = Gst.ElementFactory.make('videoconvert', 'video_convert')
    packager.pipeline.add(packager.video_convert)

    packager.video_scale = Gst.ElementFactory.make('videoscale', 'video_scale')
    packager.pipeline.add(packager.video_scale)

    packager.video_scale_caps_filter = Gst.ElementFactory.make('capsfilter', 'video_scale_caps_filter')
    packager.video_scale_caps_filter.set_property('caps', packager.video_caps)
    packager.pipeline.add(packager.video_scale_caps_filter)

    packager.video_decode_tee = Gst.ElementFactory.make('tee', '%s_video_decode_tee' % packager.name)
    packager.pipeline.add(packager.video_decode_tee)

    packager.video_fakesink = Gst.ElementFactory.make('fakesink', '%s_video_fakesink' % packager.name)
    packager.video_fakesink.set_locked_state(True)
    packager.video_fakesink.set_state(Gst.State.PAUSED)
    packager.pipeline.add(packager.video_fakesink)

    packager.video_depay.link(packager.video_dec)
    packager.video_dec.link(packager.video_rate)
    packager.video_rate.link(packager.video_convert)
    packager.video_convert.link(packager.video_scale)
    packager.video_scale.link(packager.video_scale_caps_filter)
    packager.video_scale_caps_filter.link(packager.video_decode_tee)

    video_decode_tee_srcpad_0_template = packager.video_decode_tee.get_pad_template('src_%u')
    video_decode_tee_srcpad_0 = packager.video_decode_tee.request_pad(video_decode_tee_srcpad_0_template, 'src_0')
    video_fakesink_sinkpad = packager.video_fakesink.get_static_pad('sink')
    video_decode_tee_srcpad_0.link(video_fakesink_sinkpad)

    if packager.audio_rtp_encoding_name == 'OPUS':
        packager.audio_depay = Gst.ElementFactory.make('rtpopusdepay', 'audio_depay')
        packager.audio_dec = Gst.ElementFactory.make('opusdec', 'audio_dec')

    packager.pipeline.add(packager.audio_depay)
    packager.pipeline.add(packager.audio_dec)

    packager.audio_rate = Gst.ElementFactory.make('audiorate', 'audio_rate')
    packager.pipeline.add(packager.audio_rate)

    packager.audio_convert = Gst.ElementFactory.make('audioconvert', 'audio_convert')
    packager.pipeline.add(packager.audio_convert)

    packager.audio_resample = Gst.ElementFactory.make('audioresample', 'audio_resample')
    packager.pipeline.add(packager.audio_resample)

    packager.audio_resample_caps_filter = Gst.ElementFactory.make('capsfilter', 'audio_resample_caps_filter')
    packager.audio_resample_caps_filter.set_property('caps', packager.audio_caps)
    packager.pipeline.add(packager.audio_resample_caps_filter)

    packager.audio_decode_tee = Gst.ElementFactory.make('tee', '%s_audio_decode_tee' % packager.name)
    packager.pipeline.add(packager.audio_decode_tee)

    packager.audio_fakesink = Gst.ElementFactory.make('fakesink', '%s_audio_fakesink' % packager.name)
    packager.audio_fakesink.set_locked_state(True)
    packager.audio_fakesink.set_state(Gst.State.PAUSED)
    packager.pipeline.add(packager.audio_fakesink)

    packager.audio_depay.link(packager.audio_dec)
    packager.audio_dec.link(packager.audio_rate)
    packager.audio_rate.link(packager.audio_convert)
    packager.audio_convert.link(packager.audio_resample)
    packager.audio_resample.link(packager.audio_resample_caps_filter)
    packager.audio_resample_caps_filter.link(packager.audio_decode_tee)

    audio_decode_tee_srcpad_0_template = packager.audio_decode_tee.get_pad_template('src_%u')
    audio_decode_tee_srcpad_0 = packager.audio_decode_tee.request_pad(audio_decode_tee_srcpad_0_template, 'src_0')
    audio_fakesink_sinkpad = packager.audio_fakesink.get_static_pad('sink')
    audio_decode_tee_srcpad_0.link(audio_fakesink_sinkpad)

    if packager.debug_output:
        packager.videosink = Gst.ElementFactory.make('autovideosink', 'videosink')
        packager.pipeline.add(packager.videosink)

        multi_queue_srcpad_0 = packager.multi_queue.get_static_pad('src_0')
        videosink_sinkpad = packager.videosink.get_static_pad('sink')
        multi_queue_srcpad_0.link(videosink_sinkpad)

        packager.audiosink = Gst.ElementFactory.make('autoaudiosink', 'audiosink')
        packager.pipeline.add(packager.audiosink)

        multi_queue_srcpad_1 = packager.multi_queue.get_static_pad('src_1')
        audiosink_sinkpad = packager.audiosink.get_static_pad('sink')
        multi_queue_srcpad_1.link(audiosink_sinkpad)

    else:
        # FIXME
        log_error(packager, 'hls not implemented')
        return

    packager.rtp_bin.connect('pad-added', _on_packager_rtp_bin_pad_added, packager)
    packager.rtp_bin.connect('pad-removed', _on_packager_rtp_bin_pad_removed, packager)

    packager.pipeline.set_state(Gst.State.PAUSED)

    log_graph(packager.pipeline, 'debug_packager_init')

    return packager

def do_packager_start(packager):
    log_info('do_packager_start()')
    packager.pipeline.set_state(Gst.State.PLAYING)

    log_graph(packager.pipeline, 'debug_packager_start')

def do_packager_stop(packager):
    log_info('do_packager_stop()')
    packager.pipeline.set_state(Gst.State.PAUSED)

    log_graph(packager.pipeline, 'debug_packager_stop')

def do_packager_dispose(packager):
    log_info('do_packager_dispose()')
    packager.pipeline.set_state(Gst.State.NULL)
    packager.disposed = True

    log_graph(packager.pipeline, 'debug_packager_dispose')

def _on_packager_rtp_bin_pad_added(rtp_bin, pad, packager):
    pad_name = pad.get_name()
    pad_info = parse_rtp_bin_pad_info_from_name(pad_name)

    if 'ssrc' not in pad_info: return
    log_info('_on_packager_rtp_bin_pad_added()', pad_name)

    session = pad_info.get('session')
    _on_packager_stream_start(packager, session, pad)

def _on_packager_rtp_bin_pad_removed(rtp_bin, pad, packager):
    pad_name = pad.get_name()
    pad_info = parse_rtp_bin_pad_info_from_name(pad_name)

    if 'ssrc' not in pad_info: return
    log_info('_on_packager_rtp_bin_pad_removed()', pad_name)

def _on_packager_stream_start(packager, session, srcpad):
    log_info('_on_packager_stream_start()')
    with packager.lock:
        if session not in [0, 1]:
            log_warn('session_%s' % session, 'session not found')
            return

        if session == 0:
            _do_mtunsafe_link_rtp_bin_to_rtp_decode_chain()
            _do_mtunsafe_link_rtp_decode_chain_to_input_selector()

        elif session == 1:
            pass # FIXME

def _do_mtunsafe_link_rtp_bin_to_rtp_decode_chain():
    log_info('_do_mtunsafe_link_rtp_bin_to_rtp_decode_chain()')
    pass # FIXME

def _do_mtunsafe_link_rtp_decode_chain_to_input_selector():
    log_info('_do_mtunsafe_link_rtp_decode_chain_to_input_selector()')
    pass # FIXME

def _do_mtunsafe_unlink_rtp_decode_chain_from_input_selector():
    log_info('_do_mtunsafe_unlink_rtp_decode_chain_from_input_selector()')
    pass # FIXME

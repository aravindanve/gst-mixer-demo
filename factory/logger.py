import os
import gi; gi.require_version('Gst', '1.0')
from gi.repository import Gst

class LogLevel:
    NONE = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    ALL = 4

class LogTermCode:
    RESET = '\033[0m'
    BOLD = '\033[01m'

    FG_BLACK = '\033[30m'
    FG_RED = '\033[31m'
    FG_GREEN = '\033[32m'
    FG_YELLOW = '\033[33m'
    FG_BLUE = '\033[34m'
    FG_MAGENTA = '\033[35m'
    FG_CYAN = '\033[36m'
    FG_WHITE = '\033[37m'

    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

LOG_LEVEL = LogLevel.ERROR

def set_log_level(level):
    global LOG_LEVEL
    if not level: LOG_LEVEL = LogLevel.NONE
    else: LOG_LEVEL = level

def get_log_level():
    return LOG_LEVEL

def log_error(caller, *args):
    if LOG_LEVEL < LogLevel.ERROR: return
    if hasattr(caller, 'name'):
        tag = caller.name
    elif hasattr(caller, '__name__'):
        tag = caller.__name__
    else:
        tag = caller
    print(
        LogTermCode.BG_RED, LogTermCode.BOLD, 'ERROR', LogTermCode.RESET,
        LogTermCode.FG_RED, tag, *args, LogTermCode.RESET)

def log_warn(caller, *args):
    if LOG_LEVEL < LogLevel.WARN: return
    if hasattr(caller, 'name'):
        tag = caller.name
    elif hasattr(caller, '__name__'):
        tag = caller.__name__
    else:
        tag = caller
    print(
        LogTermCode.BG_MAGENTA, LogTermCode.BOLD, 'WARNING',LogTermCode.RESET,
        LogTermCode.FG_MAGENTA, tag, *args, LogTermCode.RESET)

def log_info(caller, *args):
    if LOG_LEVEL < LogLevel.INFO: return
    tag = caller.name if hasattr(caller, 'name') else (
        caller.__name__ if hasattr(caller, '__name__') else caller)
    print(
        LogTermCode.BG_CYAN, LogTermCode.BOLD, 'INFO',LogTermCode.RESET,
        LogTermCode.FG_CYAN, tag, *args, LogTermCode.RESET)

def log_graph(gstbin, filename):
    if LOG_LEVEL < LogLevel.ALL: return
    f = open('%s.dot' % filename, 'w')
    f.write(Gst.debug_bin_to_dot_data(gstbin, Gst.DebugGraphDetails.ALL))
    f.close()

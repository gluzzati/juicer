import sys
from time import strftime


def timestamp():
    return strftime("%Y-%m-%d %H:%M:%S")


class colors:
    '''Colors class:
    reset all colors with colors.reset
    two subclasses fg for foreground and bg for background.
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


LVL_INFO = 1
LVL_OK = 0
LVL_WARN = 2
LVL_ERROR = 10

loglevel = LVL_INFO


def log(lvl, arg):
    if lvl >= loglevel:
        print("[{}] - {}".format(timestamp(), arg))
        sys.stdout.flush()


def ok(arg):
    log(LVL_OK, colors.fg.lightblue + arg + colors.reset)


def info(arg):
    log(LVL_INFO, arg)


def warn(arg):
    log(LVL_WARN, colors.fg.yellow + arg + colors.reset)


def error(arg):
    log(LVL_ERROR, colors.fg.red + arg + colors.reset)

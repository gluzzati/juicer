import sys
from time import strftime


def timestamp():
	return strftime("%H:%M:%S")


class Colors:
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


LVL_DBG = -1
LVL_OK = 0
LVL_INFO = 1
LVL_YAY = LVL_INFO
LVL_WARN = 2
LVL_ERROR = 10

logleveldict = {
    "debug": LVL_DBG,
    "ok": LVL_OK,
    "info": LVL_INFO,
    "warning": LVL_WARN,
    "error": LVL_ERROR,
}

loglevel = LVL_INFO
dbg_ctx_ref = None


def print_state(ctx):
	ret = timestamp()
	if ctx:
		state = ctx.state
		relays = ""
		for relay in ctx.relay_board.relays:
			relays += ("[" + relay + "]") if ctx.relay_board.relays[relay].pouring else ""
		ret += " {} - {}".format(state, relays)
	return ret

def log(lvl, arg):
	if lvl >= loglevel:
		print("[{}] - {}".format(print_state(dbg_ctx_ref), arg))
		sys.stdout.flush()


def debug(arg):
	log(LVL_DBG, Colors.fg.darkgrey + arg + Colors.reset)


def ok(arg):
	log(LVL_OK, Colors.fg.lightblue + arg + Colors.reset)


def info(arg):
	log(LVL_INFO, arg)


def yay(arg):
	log(LVL_YAY, Colors.fg.lightgreen + arg + Colors.reset)


def warn(arg):
	log(LVL_WARN, Colors.fg.yellow + arg + Colors.reset)


def error(arg):
	log(LVL_ERROR, Colors.fg.red + arg + Colors.reset)

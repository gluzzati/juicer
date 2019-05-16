from time import strftime

def timestamp():
	return strftime("%Y-%m-%d %H:%M:%S")

LVL_INFO = 1
LVL_ERROR = 10

loglevel = LVL_INFO

def log(lvl, arg):
	if lvl > loglevel:
		print("[{}] - {}".format(timestamp(), arg))

def info(arg):
	log(LVL_INFO, arg)

def error(arg):
	log(LVL_ERROR, arg)

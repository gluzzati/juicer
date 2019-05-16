from . import log
from . import message
from . import result

Result = result.Result
Message = message.Message
error = log.error
log = log.log

def get_msg():
	pass

def is_valid(msg):
	if not isinstance(msg, Message):
		return False
	return True

def handle_msg(mainloop, msg):
	result = Result()
	if not is_valid(msg):
		result.ok = False
		return result
	log(msg.type)
	handler = get_handler(msg.type)
	if handler == null:
		result.ok = False
		return result
	else:
		result = handler(msg)
		return result

class Mainloop:
	def __init__(self):
		self.running = True

	def run(self, args):

		while self.running:
			msg = get_msg()
			result = handle_msg(self, msg)
			if not result.ok:
				error("error handling message")
		return 0


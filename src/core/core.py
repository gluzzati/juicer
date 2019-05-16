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

	log(msg.type)

	if msg.type not in mainloop.handlers:
		result.ok = False
		return result
	else:
		handler = mainloop[msg.type]
		result = handler(msg)
		return result

class Mainloop:
	def __init__(self):
		self.running = True
		self.handlers = load_handlers()

	def run(self, args):

		while self.running:
			msg = get_msg()
			result = handle_msg(self, msg)
			if not result.ok:
				error("error handling message")
		return 0


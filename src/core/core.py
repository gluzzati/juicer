import math

from core import log
from core.event import Event

MAX = int(math.pow(2, 16))  # 64K


def get_evt(ctx):
	evt = ctx.queue.get(True)

	if not isinstance(evt, Event):
		log.error("not an event (" + str(type(evt)) + ")")
		return False, None

	if evt.type == Event.SIGINT:
		ctx.running = False
		return False, None

	return True, evt


def unknown_event(evt):
	log.error("unknown evt \"" + evt.type + "\"")


class Core:
	def __init__(self, context):
		self.ctx = context
		self.ctx.running = True
		self.handlers = dict()
		self.handle_unknown_evt = unknown_event

	def add_handler(self, evt_type, handler):
		self.handlers[evt_type] = handler

	def run(self):

		while self.ctx.running:
			ok, evt = get_evt(self.ctx)

			if not ok:
				continue

			if evt.type not in self.handlers:
				self.handle_unknown_evt(evt)
				continue

			self.handlers[evt.type](evt)

		return 0

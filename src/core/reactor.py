import math

from core import log
from core.events import Event, Handlers

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


class Reactor:
	def __init__(self, context):
		self.ctx = context
		self.ctx.running = True
		self.handlers = dict()
		self.handle_unknown_evt = Handlers.unknown_event

	def add_handler(self, evt_type, handler):
		self.handlers[evt_type] = handler

	def run(self):
		while self.ctx.running:
			ok, evt = get_evt(self.ctx)

			if not ok:
				continue

			if evt.type not in self.handlers:
				ok, res = self.handle_unknown_evt(self.ctx, evt)
				continue

			ok, res = self.handlers[evt.type](self.ctx, evt)

		return 0

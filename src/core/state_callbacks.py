import time
from threading import Thread

from core import log
from core.context import Context
from core.events import Event

SAFETY_TIMEOUT = 5
GUARD = 0.9


class Safety(Thread):
	def __init__(self, relay, scale, glass, queue):
		self.relay = relay
		self.scale = scale
		self.glass = glass
		self.queue = queue
		super().__init__()

	def glass_full(self):
		return self.scale.get_weight() > (GUARD * (self.glass.weight + self.glass.capacity))

	def run(self):
		start = time.time()
		elapsed = time.time() - start
		while elapsed < SAFETY_TIMEOUT and self.relay.pouring and not self.glass_full():
			time.sleep(0.1)
			elapsed = time.time() - start

		if self.relay.pouring:
			self.relay.water_off()
			evt = Event(Event.AUTO_WATEROFF)
			evt.cause = None
			log.warn("auto off")
			if elapsed > SAFETY_TIMEOUT:
				log.warn("timed out")
				evt.cause = "TIMEOUT"
			if self.glass_full():
				log.warn("glass full")
				evt.cause = "GLASS_FULL"
			self.queue.put(evt)


def on_idle(ctx):
	log.debug("on idle")
	ctx.user = None
	ctx.state = Context.State.IDLE
	return True, None


def on_glass_on(ctx):
	log.debug("on glass on")
	ctx.state = Context.State.GLASS_ON
	return True, None


def on_pouring(ctx):
	log.debug("on pouring")
	timer = Safety(ctx.relay, ctx.scale, ctx.user.glass, ctx.queue)
	ctx.state = Context.State.POURING
	ctx.relay.water_on()
	timer.start()
	return True, None

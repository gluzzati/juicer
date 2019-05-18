import time
from queue import Queue
from threading import Thread

from core import log
from core.database import Database
from core.events import Event
from gui.gui import GuiProxy
from relay.relay import Relay
from scale.scale import Scale

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


class Context:
	class State:
		UNINIT = "UNINIT"
		IDLE = "IDLE"
		GLASS_ON = "GLASS_ON"
		POURING = "POURING"

		ALLOWABLE = [
			UNINIT,
			IDLE,
			GLASS_ON,
			POURING,
		]

	@staticmethod
	def is_valid_state(state):
		if not isinstance(state, str):
			return False
		return state in Context.State.ALLOWABLE

	def initialize(self):
		self.state = Context.State.IDLE

	def __init__(self):
		self.valid = True
		self.state = Context.State.UNINIT
		self.gui = GuiProxy()
		self.database = Database()
		self.user = None

		# todo delete
		from core.user import User
		giulio = User()
		giulio.name = "Giulio"
		giulio.tag = 797313096147
		giulio.glass.capacity = 250
		giulio.glass.weight = 280
		self.database.add(giulio)

		self.scale = Scale()
		self.queue = Queue()
		self.relay = Relay()
		self.relay.set_pourer(2)
		self.initialize()

		self.state_callbacks = {
			Context.State.IDLE: self.on_idle,
			Context.State.GLASS_ON: self.on_glass_on,
			Context.State.POURING: self.on_pouring,
		}

	def set_scale(self, scale):
		if not isinstance(scale, Scale):
			log.error("trying to set scale with wrong type " + str(type(scale)))
			pass
		else:
			self.scale = scale

	def get_state(self):
		return self.state

	def set_state(self, state):
		if isinstance(state, type(Context.State.IDLE)):
			if self.state != state:
				self.state = state
				self.state_callbacks[self.state]()
		else:
			log.debug("trying to set state using a wrong type, aborting")

		pass

	def start_pouring(self):
		log.ok("issuing startpour")
		self.set_state(Context.State.POURING)

	def stop_pouring(self):
		log.ok("issuing stoppouring")
		self.set_state(Context.State.IDLE)

	"""
	state change callbacks
	"""

	def on_idle(self):
		log.debug("on idle")
		self.user = None
		pass

	def on_glass_on(self):
		log.debug("on glass on")
		pass

	def on_pouring(self):
		log.debug("on pouring")
		timer = Safety(self.relay, self.scale, self.user.glass, self.queue)
		self.relay.water_on()
		timer.start()
		pass

from queue import Queue

from core import log
from core.database import Database
from scale.scale import Scale


class Context:
	class State:
		UNINIT = "UNINIT"
		IDLE = "IDLE"
		GLASS_ON = "GLASS_ON"
		POURING = "POURING"
		REGISTERING = "REGISTERING"

		ALLOWABLE = [
			UNINIT,
			IDLE,
			GLASS_ON,
			POURING,
			REGISTERING,
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
		self.database = Database()
		self.scale = Scale()
		self.queue = Queue()
		self.gui = None

		self.state_callbacks = {
			Context.State.IDLE: self.on_idle,
			Context.State.GLASS_ON: self.on_glass_on,
			Context.State.POURING: self.on_pouring,
			Context.State.REGISTERING: self.on_registering,
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
			self.state = state
			self.state_callbacks[self.state]()
		else:
			log.debug("trying to set state using a wrong type, aborting")

		pass

	def start_pouring(self):
		log.ok("issuing startpour")

	def stop_pouring(self):
		log.ok("issuing stoppouring")

	"""
	state change callbacks
	"""

	def on_idle(self):
		log.debug("on idle")
		pass

	def on_glass_on(self):
		log.debug("on glass on")
		pass

	def on_pouring(self):
		log.debug("on pouring")
		pass

	def on_registering(self):
		log.debug("on registering")
		pass

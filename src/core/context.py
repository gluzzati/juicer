from queue import Queue

from core import log
from core.database import Database
from gui.gui import GuiProxy
from relay.relay import Relay
from scale.scale import Scale


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
		# todo delete
		from core.user import User
		giulio = User()
		giulio.name = "Giulio"
		giulio.tag = 797313096147
		giulio.glass_capacity = 250
		giulio.glass_weight = 280
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
			self.state = state
			self.state_callbacks[self.state]()
		else:
			log.debug("trying to set state using a wrong type, aborting")

		pass

	def start_pouring(self):
		log.ok("issuing startpour")
		self.relay.water_on()

	def stop_pouring(self):
		log.ok("issuing stoppouring")
		# todo readd
		self.relay.water_off()

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

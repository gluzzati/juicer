from core import log
from core.database import Database
from core.water_machine import WaterMachine
from scale.scale import Scale


class Context:
	def __init__(self, args):
		self.args = args
		self.valid = True
		self.state_machine = WaterMachine()
		self.database = Database()
		self.scale = None
		self.gui = None

	def set_scale(self, scale):
		if not isinstance(scale, Scale):
			log.error("trying to set scale with wrong type " + str(type(scale)))
			pass
		else:
			self.scale = scale

	def get_state(self):
		return self.state_machine.state

	def set_state(self, state):
		if not isinstance(state, type(WaterMachine.State.IDLE)):
			log.debug("trying to set state using a wrong type, aborting")
			pass
		else:
			self.state_machine.state = state

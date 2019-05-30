import os
from queue import Queue

from core.database import Database
from flow_meter.flowmeter import FlowMeter
from gui.gui import GuiProxy
from relay.relay import Relay
from scale.scale import Scale

CWD = os.getcwd() + "/"

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

	def __init__(self, args):
		self.args = args
		self.valid = True
		self.state = Context.State.UNINIT
		self.gui = GuiProxy()
		self.database = Database()
		self.user = None
		self.scale = Scale()
		self.queue = Queue()
		self.relay = Relay()
		self.relay.set_pourer(2)
		self.initialize()
		self.flowmeter = FlowMeter(18, 4.25)  # todo: dehardcode pin

class WaterMachine:
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
		return state in WaterMachine.State.ALLOWABLE

	def __init__(self):
		self.state = WaterMachine.State.UNINIT

	def initialize(self):
		self.state = WaterMachine.State.IDLE

from core import log


class StateMachine:
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
		return state in StateMachine.State.ALLOWABLE

	def __init__(self):
		self.state = StateMachine.State.UNINIT

	def initialize(self):
		self.state = StateMachine.State.IDLE

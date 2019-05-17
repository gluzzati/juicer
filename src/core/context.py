from core.state_machine import StateMachine


class Context:
	def __init__(self, args):
		self.args = args
		self.valid = True
		self.state_machine = StateMachine()

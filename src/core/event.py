from core.state_machine import StateMachine
from core import log


class Event:
	SIGINT = "SIGINT"
	JSON = "JSON"
	RFID_DETECTED = "RFID_DETECTED"
	INVALID = "INVALID"

	def __init__(self):
		self.data = None
		self.type = Event.INVALID


class Handlers:
	@staticmethod
	def rfid_detected(ctx, evt):
		log.info("rfid detected: " + str(evt.rfid))
		ok = True

		if ctx.state_machine.state != StateMachine.State.IDLE:
			log.error("machine not ready! " + ctx.state_machine.state)
			ok = False
		else:
			ctx.state_machine.state = StateMachine.State.GLASS_ON

		out = dict()
		return ok, out

	@staticmethod
	def unknown_event(ctx, evt):
		log.error("unknown evt \"" + evt.type + "\"")
		return False, None

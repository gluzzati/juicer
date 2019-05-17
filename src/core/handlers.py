from core import log
from core.state_machine import StateMachine


class Result:
	def __init__(self):
		self.ok = None


def rfid_detected(ctx, evt):
	log.info("rfid detected: " + str(evt.rfid))
	ok = True

	if ctx.state_machine.state != StateMachine.State.IDLE:
		log.error("machine not ready! " + ctx.state_machine.state)
		ok = False
	else:
		ctx.state_machine.state = StateMachine.State.GLASS_ON

	out = Result()
	out.ok = ok
	return out

from core import log


class Result:
	def __init__(self):
		self.ok = None


def rfid_detected(evt):
	log.info("rfid detected: " + str(evt.rfid))
	out = Result()
	out.ok = True
	return out

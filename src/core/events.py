import time

from core import log

OBLIVION = 2  # seconds

class Event:
	SIGINT = "SIGINT"
	JSON = "JSON"
	RFID_DETECTED = "RFID_DETECTED"
	RFID_REMOVED = "RFID_REMOVED"
	WEIGHT_MEASURE = "WEIGHT_MEASURE"
	REGISTRATION_REQUESTED = "REGISTRATION_REQUESTED"
	AUTO_WATEROFF = "AUTO_WATEROFF"
	INVALID = "INVALID"

	def __init__(self, type):
		self.timestamp = time.time()  # slow?
		self.data = None
		self.type = type

	def too_old(self):
		is_old = time.time() - self.timestamp > OBLIVION
		if is_old:
			log.info("discarding old event " + self.type)
		return is_old

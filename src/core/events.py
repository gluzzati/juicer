import time


class Event:
	SIGINT = "SIGINT"
	JSON = "JSON"
	RFID_DETECTED = "RFID_DETECTED"
	RFID_REMOVED = "RFID_REMOVED"
	WEIGHT_MEASURE = "WEIGHT_MEASURE"
	REGISTRATION_REQUESTED = "REGISTRATION_REQUESTED"
	INVALID = "INVALID"

	def __init__(self, type):
		self.timestamp = time.time()  # slow?
		self.data = None
		self.type = type

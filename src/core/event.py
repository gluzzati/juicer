class Event:
	SIGINT = "SIGINT"
	JSON = "JSON"
	RFID_DETECTED = "RFID_DETECTED"
	INVALID = "INVALID"

	def __init__(self):
		self.data = None
		self.type = Event.INVALID

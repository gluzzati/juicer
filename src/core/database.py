from core import log


class Database:
	def __init__(self):
		self.table = dict()

	def lookup_rfid(self, rfid):
		if not isinstance(rfid, str):
			log.error("trying to lookup rfid with type " + str(type(rfid)))
			return False, None
		if rfid in self.table:
			return True, self.table[rfid]
		else:
			log.debug("not in DB " + rfid)
			return False, None

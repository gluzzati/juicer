from core import log
from core.user import User


class Database:
	def __init__(self):
		self.table = dict()

	def lookup_rfid(self, rfid):
		if not isinstance(rfid, int):
			log.error("trying to lookup rfid with type " + str(type(rfid)))
			return False, None
		if rfid in self.table:
			return True, self.table[rfid]
		else:
			log.debug("not in DB " + str(rfid))
			return False, None

	def add_user(self, user):
		if not isinstance(user, User):
			log.error("trying to add user with wrong type " + str(type(user)))
			return False
		if not user.is_valid():
			log.error("user contains invalid data")
			return False

		self.table[user.tag] = user

		log.debug("successfully added " + user.name + " to database")
		return True

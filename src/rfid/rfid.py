import RPi.GPIO as GPIO

from core import log
from rfid.mfrc522 import SimpleMFRC522


class RFID:
	def __init__(self):
		self.reader = SimpleMFRC522()

	def __del__(self):
		GPIO.cleanup()

	def read_id(self):
		try:
			tag = self.reader.read_id()
			res = True
		except Exception as e:
			log.error("error reading rfid: " + str(e))
			tag = None
			res = False

		return res, tag

	def read_id_no_block(self):
		try:
			tag = self.read_id_no_block()
			res = True
		except Exception as e:
			log.error("error reading rfid: " + str(e))
			tag = None
			res = False

		return res, tag

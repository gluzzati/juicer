import time
from threading import Thread

import RPi.GPIO as GPIO

from core import log

SAFETY_TIMEOUT = 30


class SafetyTimer(Thread):
	def __init__(self, relay):
		self.relay = relay
		super().__init__()

	def run(self):
		start = time.time()
		while time.time() - start < SAFETY_TIMEOUT and self.relay.pouring:
			time.sleep(1)
		if self.relay.pouring:
			log.warn("safety stop triggered!")
			self.relay.water_off()


class Relay:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.pourer_pin = None

	def enable(self, pin):
		if not isinstance(pin, int):
			log.error("error setting pin, type must be int! " + str(type(pin)))
			return False
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
		return True

	def set_pourer(self, pin):
		if self.enable(pin):
			log.debug("pourer relay set to pin " + str(pin))
			self.pourer_pin = pin

	def water_on(self):
		if self.pourer_pin:
			self.pouring = True
			GPIO.output(self.pourer_pin, GPIO.LOW)
			timer = SafetyTimer(self)
			timer.start()

	def water_off(self):
		if self.pourer_pin:
			self.pouring = False
			GPIO.output(self.pourer_pin, GPIO.HIGH)

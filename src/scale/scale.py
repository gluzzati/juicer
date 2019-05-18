from threading import Thread

import RPi.GPIO as GPIO

from core.events import Event
from scale.hx711.hx711 import HX711

DOUT = 23
SCK = 24
UNIT_SCALE = 730


class FakeScale:
	def __init__(self):
		pass

	def reset_and_tare(self):
		pass

	def get_weight(self):
		return 11


class Scale:
	def __init__(self):
		self.hx = HX711(DOUT, SCK)
		self.hx.set_reading_format("MSB", "MSB")
		self.hx.set_reference_unit(UNIT_SCALE)
		self.reset_and_tare()
		self.init = True

	def reset_and_tare(self):
		self.hx.reset()
		self.hx.tare()

	def __del__(self):
		GPIO.cleanup()

	def get_weight(self):
		return self.hx.get_weight(3)


def request_weight_measure(scale, queue):
	weight = scale.get_weight()
	evt = Event(Event.WEIGHT_MEASURE)
	evt.weight = weight
	queue.put(evt)


class ScaleThread(Thread):
	def __init__(self, mainqueue):
		self.mainqueue = mainqueue
		self.running = False
		super().__init__()

	def stop(self):
		self.running = False

	def run(self):
		self.running = True
		while self.running:
			pass

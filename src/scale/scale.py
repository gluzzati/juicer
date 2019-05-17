import RPi.GPIO as GPIO

from scale.hx711.hx711 import HX711

DOUT = 23
SCK = 24
UNIT_SCALE = 730


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
		return self.hx.get_weight()


class ScaleEmulator(Scale):
	def get_weight(self):
		return 10

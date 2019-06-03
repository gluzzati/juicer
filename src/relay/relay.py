import RPi.GPIO as GPIO

from core import log


class Relay:
    def __init__(self, flowmeter, pin):
        GPIO.setmode(GPIO.BCM)
        self.flowmeter = flowmeter
        self.pourer_pin = None
        self.set_pourer(pin)
        self.pouring = False

    def __enable(self, pin):
        if not isinstance(pin, int):
            log.error("error setting pin, type must be int! " + str(type(pin)))
            return False
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        return True

    def set_pourer(self, pin):
        if self.__enable(pin):
            log.debug("pourer relay set to pin " + str(pin))
            self.pourer_pin = pin

    def liquid_on(self):
        if self.pourer_pin:
            self.pouring = True
            GPIO.output(self.pourer_pin, GPIO.LOW)

    def liquid_off(self):
        if self.pourer_pin:
            self.pouring = False
            GPIO.output(self.pourer_pin, GPIO.HIGH)

    def pour(self, cc):
        self.flowmeter.reset()
        self.flowmeter.enable()
        self.liquid_on()
        while self.flowmeter.poured_ccs() < cc:
            pass
        self.liquid_off()
        self.flowmeter.reset()
        self.flowmeter.disable()


class RelayBoard:
    def __init__(self, relaylist, flowmeter):
        self.relays = dict()
        for name, pin in relaylist:
            self.relays[name] = Relay(flowmeter, pin)

    def pouring(self):
        for relay in self.relays:
            if self.relays[relay].pouring:
                return True

        return False

    def liquid_off(self):
        for relay in self.relays:
            self.relays[relay].liquid_off()

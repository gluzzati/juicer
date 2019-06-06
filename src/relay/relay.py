import RPi.GPIO as GPIO

from core import log


class Relay:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
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

    def open(self):
        if self.pourer_pin:
            self.pouring = True
            GPIO.output(self.pourer_pin, GPIO.LOW)

    def close(self):
        if self.pourer_pin:
            self.pouring = False
            GPIO.output(self.pourer_pin, GPIO.HIGH)


class RelayBoard:
    def __init__(self, relaylist):
        self.relays = dict()
        for name, pin in relaylist:
            self.relays[name] = Relay(pin)

    def pouring(self):
        for relay in self.relays:
            if self.relays[relay].pouring:
                return True

        return False

    def shut_all(self):
        for relay in self.relays:
            self.relays[relay].close()

    def open(self, name):
        if name in self.relays:
            self.relays[name].open()
        else:
            log.error("no known tap for \"" + name + "\"")

    def close(self, name):
        if name in self.relays:
            self.relays[name].close()
        else:
            log.error("no known tap for \"" + name + "\"")

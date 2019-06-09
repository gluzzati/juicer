from RPi import GPIO

from core import log


class FlowMeter:
    def __init__(self, GPIO_PIN, pulses_per_cc=4.25):
        self.pulse_count = 0
        self.tared = True
        self.tcc = pulses_per_cc
        self.pin = GPIO_PIN
        self.enabled = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def enable(self):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.increment)
        self.enabled = True

    def disable(self):
        GPIO.remove_event_detect(self.pin)
        self.enabled = False

    def reset(self):
        self.pulse_count = 0

    def increment(self, channel):
        self.pulse_count += 1
        log.ok("count: " + str(self.pulse_count))
        log.ok("poured {} ccs".format(self.poured_ccs()))

    def poured_ccs(self):
        if self.tared:
            return self.pulse_count / self.tcc
        else:
            return 0

    def tare(self, cc):
        try:
            self.tcc = self.pulse_count / cc
            log.ok("updated self.tcc to " + str(self.tcc))
            self.tared = True
        except TypeError:
            log.warn("trying to tare with wrong type")

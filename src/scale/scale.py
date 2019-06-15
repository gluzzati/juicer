from threading import Thread

from core import log
from core.events import create_event, EventType, EventKey
from scale.hx711.hx711 import HX711


class FakeScale:
    def __init__(self):
        pass

    def reset_and_tare(self):
        pass

    def get_weight(self):
        return 286.5


class Scale:
    def __init__(self, config):
        scale_cfg = config["scale"]
        DOUT = int(scale_cfg["DOUT"])
        SCK = int(scale_cfg["SCK"])
        SCALE_CONSTANT = int(scale_cfg["conversion_constant"])
        self.hx = HX711(DOUT, SCK)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(SCALE_CONSTANT)
        self.reset_and_tare()
        self.init = True

    def reset_and_tare(self):
        self.hx.reset()
        log.debug("taring scale... ")
        self.hx.tare()
        log.debug("tare complete, scale ready")
        while True:
            log.yay("weight: " + str(self.hx.get_weight()))

    def get_weight(self):
        return self.hx.get_weight(1)


def request_weight_measure(scale, queue):
    weight = scale.get_weight()
    evt = create_event(EventType.WEIGHT_MEASURE)
    evt[EventKey.weight] = weight
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

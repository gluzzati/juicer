from threading import Thread

from core import log
from core.events import EventType, create_event, EventKey
from rfid.mfrc522 import SimpleMFRC522


class RFID:
    def __init__(self):
        self.reader = SimpleMFRC522()
        self.history = 0

    def read_id(self):
        try:
            tag = self.reader.read_id(0.005)
            res = True

        except Exception as e:
            log.error("error reading rfid: " + str(e))
            tag = None
            res = False

        return res, tag

    def read_id_no_block(self):
        try:
            tag = self.reader.read_id_no_block()
            res = True
        except Exception as e:
            log.error("error reading rfid: " + str(e))
            tag = None
            res = False

        return res, tag


class RfidThread(Thread):
    def __init__(self, queue):
        self.running = False
        self.rfid = RFID()
        self.queue = queue
        self.tag_present = False
        self.current_tag = None

        super().__init__()

    def dispatch(self, evt):
        log.debug("dispatching " + evt[EventKey.type])
        self.queue.put(evt)

    def run(self):
        self.running = True
        while self.running:
            ok, tag = self.rfid.read_id()
            detected = tag is not None

            if detected and (not self.tag_present or tag != self.current_tag):
                evt = create_event(EventType.RFID_DETECTED)
                evt[EventKey.rfid] = tag
                self.current_tag = tag
                self.tag_present = True
                self.dispatch(evt)
            elif detected and tag != self.current_tag:
                evt = create_event(EventType.RFID_DETECTED)
                evt[EventKey.rfid] = tag
                self.current_tag = tag
                self.dispatch(evt)

            elif not detected and self.tag_present:
                evt = create_event(EventType.RFID_REMOVED)
                self.current_tag = None
                self.tag_present = False
                self.dispatch(evt)

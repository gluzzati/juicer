import json
from core import log
from core import handlers
from types import SimpleNamespace as Namespace

KILLMSG = "@@__DIENOW__PLEASE__@@"


class Message:
    def __init__(self, string):
        if not isinstance(string, str):
            log.error("not a string")
            self.valid = False
            return

        try:
            self.values = json.loads(string, object_hook=lambda d: Namespace(**d))
            self.valid = True
        except json.decoder.JSONDecodeError:
            log.error("error decoding msg: " + str(string))
            self.valid = False
            return

        try:
            self.type = self.values.type
        except Exception as e:
            log.error("exception: " + str(e))
            self.valid = False

    def to_json(self):
        return json.dumps(self.values)


class MsgTypes:
    INVALID = -1
    WEIGHT_UPDATE = 1
    RFID_DETECTED = 2


handlers = {
    MsgTypes.INVALID: handlers.invalid,
    MsgTypes.WEIGHT_UPDATE: handlers.weight_updated,
    MsgTypes.RFID_DETECTED: handlers.rfid_detected,
}

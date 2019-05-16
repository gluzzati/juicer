import json
from core import log
from types import SimpleNamespace as Namespace
from core import result


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


def invalid_h(msg):
    log.info("no handler for type " + str(msg.values.type))
    out = result.Result()
    return out


def weight_updated_h(msg):
    log.info("weight update received: " + str(msg.values.weight))
    out = result.Result()
    out.ok = True
    return out


def rfid_detected_h(msg):
    log.info("rfid detected: " + str(msg.values.rfid))
    out = result.Result()
    out.ok = True
    return out


handlers = {
    MsgTypes.INVALID: invalid_h,
    MsgTypes.WEIGHT_UPDATE: weight_updated_h,
    MsgTypes.RFID_DETECTED: rfid_detected_h,
}

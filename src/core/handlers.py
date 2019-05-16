from core import log
from core import result


def invalid(msg):
    log.info("no handler for type " + str(msg.values.type))
    out = result.Result()
    return out


def weight_updated(msg):
    log.info("weight update received: " + str(msg.values.weight))
    out = result.Result()
    out.ok = True
    return out


def rfid_detected(msg):
    log.info("rfid detected: " + str(msg.values.rfid))
    out = result.Result()
    out.ok = True
    return out

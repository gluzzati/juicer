import json
import time

from core import log

OBLIVION = 2  # seconds


class EventKey:
    timestamp = "timestamp"
    type = "type"
    weight = "weight"
    user = "user"
    rfid = "rfid"
    cause = "cause"


class EventType:
    SIGINT = "SIGINT"
    JSON = "JSON"
    RFID_DETECTED = "RFID_DETECTED"
    RFID_REMOVED = "RFID_REMOVED"
    WEIGHT_MEASURE = "WEIGHT_MEASURE"
    REGISTRATION_REQUESTED = "REGISTRATION_REQUESTED"
    AUTO_WATEROFF = "AUTO_WATEROFF"
    POUR_REQUESTED = "POUR_REQUESTED"
    INVALID = "INVALID"


def create_event(type):
    evt = dict()
    evt[EventKey.type] = type
    evt[EventKey.timestamp] = time.time()
    return evt


def too_old(evt):
    is_old = time.time() - evt[EventKey.timestamp] > OBLIVION
    if is_old:
        log.info("discarding old event " + evt[EventKey.type])
    return is_old


def evt2json(evt):
    return json.dumps(evt, default=lambda o: o.__dict__)


def json2evt(json_string):
    return json.loads(json_string)

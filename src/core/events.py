import json
import time

from core import log

OBLIVION = float('inf')  # seconds


class EventKey:
    timestamp = "timestamp"
    type = "type"
    weight = "weight"
    user = "user"
    rfid = "rfid"
    cause = "cause"
    requested_recipe = "requested_recipe"
    add_recipe = "add_recipe"


RequiredEventKeys = [EventKey.timestamp, EventKey.type]


def validate(evt):
    for key in RequiredEventKeys:
        if key not in evt:
            return False

        # if type(evt[EventKey.timestamp]) is not (float or int):
        #     return False

    return True


class EventType:
    SIGINT = "SIGINT"
    JSON = "JSON"
    RFID_DETECTED = "RFID_DETECTED"
    RFID_REMOVED = "RFID_REMOVED"
    WEIGHT_MEASURE = "WEIGHT_MEASURE"
    NEW_USER = "NEW_USER"
    AUTO_WATEROFF = "AUTO_WATEROFF"
    NEW_RECIPE = "NEW_RECIPE"
    POUR_REQUESTED = "POUR_REQUESTED"
    INVALID = "INVALID"
    POUR_COMPLETED = "POUR_COMPLETED"


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
    try:
        out = json.loads(json_string)
        return True, out
    except json.decoder.JSONDecodeError as e:
        log.error("error converting json to evt: " + str(e))
        return False, None

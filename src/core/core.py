import errno

from . import log
from . import message
from . import result
import os
import math

Result = result.Result
Message = message.Message

PATH = "./pipe"
try:
    os.mkfifo(PATH)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

MAX = int(math.pow(2, 19))  # 512K


def get_msg():
    pipe = os.open(PATH, os.O_RDONLY)
    data = os.read(pipe, MAX)
    os.close(pipe)
    return Message(data.decode())


def get_handler(type):
    if type not in message.handlers:
        return message.handlers[message.MsgTypes.INVALID]
    else:
        return message.handlers[type]


def handle_msg(mainloop, msg):
    result = Result()

    if not isinstance(msg, Message):
        log.error("invalid message")
        result.ok = False
        return result

    handler = get_handler(msg.type)
    try:
        res = handler(msg)
    except AttributeError as e:
        log.error("malformed object")
        log.error(str(e))
        res = Result()
        res.ok = False

    return res


class Mainloop:
    def __init__(self):
        self.running = True

    def run(self, args):

        while self.running:
            msg = get_msg()
            if msg.valid:
                result = handle_msg(self, msg)
                if not result.ok:
                    log.error("error handling message")

        return 0

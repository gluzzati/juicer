import errno
import math
import os

from . import log
from . import message
from . import result

Result = result.Result
Message = message.Message

PATH = "pipe"
try:
    os.mkfifo(PATH)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

MAX = int(math.pow(2, 19))  # 512K


def get_msg(ctx):
    data, addr = ctx.sock.recvfrom(MAX)
    return Message(data.decode())


def get_handler(msgtype):
    if msgtype not in message.handlers:
        return message.handlers[message.MsgTypes.INVALID]
    else:
        return message.handlers[msgtype]


def handle_msg(ctx, msg):
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
    def __init__(self, context):
        self.running = True
        self.ctx = context

    def run(self, args):

        while self.running:
            msg = get_msg(self.ctx)
            if msg.valid:
                result = handle_msg(self.ctx, msg)
                if not result.ok:
                    log.error("error handling message")

        return 0

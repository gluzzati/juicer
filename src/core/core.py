import math

from . import log
from . import message
from . import result

Result = result.Result
Message = message.Message

MAX = int(math.pow(2, 16))  # 64K


def get_msg(ctx):
    data, addr = ctx.sock.recvfrom(MAX)

    if data.decode() == message.KILLMSG:
        ctx.running = False
        return False, None

    return True, Message(data.decode())


def get_handler(msgtype):
    if msgtype not in message.handlers:
        return message.handlers[message.MsgTypes.INVALID]
    else:
        return message.handlers[msgtype]


def handle_msg(ctx, msg):

    if not isinstance(msg, Message):
        log.error("invalid message")
        result = Result()
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
        self.ctx = context
        self.ctx.running = True

    def run(self):

        while self.ctx.running:
            ok, msg = get_msg(self.ctx)
            if not ok:
                continue
            if msg.valid:
                res = handle_msg(self.ctx, msg)
                if not res.ok:
                    log.error("error handling message")

        return 0

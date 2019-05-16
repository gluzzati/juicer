#!/usr/bin/python3
import socket
import threading

from core.context import Context
from core.core import Mainloop
from core.message import KILLMSG
from var import test_fixtures


class Object(object):
    pass


args = Object()
args.port = 5555


class MainThread(threading.Thread):
    def run(self):
        context = Context(args)
        loop = Mainloop(context)
        return loop.run()


def send_msg(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(str.encode(msg), ("localhost", args.port))


def main():
    main_t = MainThread()
    main_t.start()

    send_msg(test_fixtures.invalid_json)
    send_msg(test_fixtures.rfid_json)
    send_msg(test_fixtures.weight_json)
    send_msg(test_fixtures.valid_json)

    send_msg(KILLMSG)

    main_t.join()


if __name__ == "__main__":
    main()

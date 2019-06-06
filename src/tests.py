#!/usr/bin/python3
import argparse
import sys
import threading
import time
from queue import Queue

import yaml

from core.event_handlers import *
from core.faucet import Faucet, Recipe
from core.reactor import Reactor
from core.user import User
from gui.gui import GuiProxy
from relay.relay import Relay, RelayBoard
from rfid.rfid import RFID
from scale.scale import FakeScale

log.loglevel = log.LVL_DBG

# globally expose internals
main_queue = Queue()
context = Context(None)


class MainThread(threading.Thread):
    def __init__(self):
        self.queue = None
        self.retcode = None
        super().__init__()

    def set_queue(self, queue):
        self.queue = queue

    def run(self):
        context.queue = self.queue
        consumer = Reactor(context)
        consumer.add_handler(EventType.RFID_DETECTED, rfid_detected_handler)
        context.scale = FakeScale()
        context.gui = GuiProxy()
        self.retcode = consumer.run()
        return


def qpush(evt):
    main_queue.put(evt)
    time.sleep(0.001)


def send_json_msg(msg, queue):
    evt = create_event(EventType.JSON)
    evt["data"] = str.encode(msg)
    qpush(evt)


def send_rfid(rfid, queue):
    evt = create_event(EventType.RFID_DETECTED)
    evt[EventKey.rfid] = rfid
    qpush(evt)


def send_killevt(queue):
    evt = create_event(EventType.SIGINT)
    qpush(evt)


def send_rfid_removed(queue):
    evt = create_event(EventType.RFID_REMOVED)
    qpush(evt)


def send_invalid(queue):
    evt = create_event(EventType.INVALID)
    evt["type"] = "what is this?"
    qpush(evt)


def send_wrong_type(queue):
    evt = "not an event"
    qpush(evt)


def send_register(queue):
    evt = create_event(EventType.REGISTRATION_REQUESTED)
    giulio = User()
    giulio.name = "Giulio"
    giulio.tag = 797313096147
    giulio.glass.capacity = 250
    giulio.glass.weight = 280
    evt[EventKey.user] = giulio
    qpush(evt)


def timeout(tout, a, b):
    start = time.time()
    while time.time() - start < tout:
        if a == b:
            return True
        time.sleep(0.000001)
    return False


def core_test():
    main_t = MainThread()
    main_t.set_queue(main_queue)
    main_t.start()

    send_invalid(main_queue)
    assert (context.state == Context.State.IDLE)

    send_wrong_type(main_queue)
    assert (context.state == Context.State.IDLE)

    send_rfid(565454684, main_queue)
    assert (context.state == Context.State.GLASS_ON)

    context.initialize()
    send_rfid(797313096147, main_queue)
    assert (timeout(0.01, context.state, Context.State.GLASS_ON))

    send_register(main_queue)
    assert (timeout(0.01, context.state, Context.State.GLASS_ON))

    send_rfid_removed(main_queue)
    assert (timeout(0.01, context.state, Context.State.IDLE))

    # send_rfid(797313096147, main_queue)
    # assert (timeout(0.01, context.state, Context.State.GLASS_ON))

    send_killevt(main_queue)
    main_t.join()
    assert (main_t.retcode == 0)


def scale_test():
    log.ok("testing scale..")
    scale = context.scale
    for i in range(3):
        w = scale.get_weight()
        log.ok("weight = " + str(w))
        assert w is not None


def rfid_test():
    bluefob = 797313096147
    log.ok("testing rfid - approach blue fob (tag n. {}), press any key when ready".format(bluefob))
    input()
    rfid = RFID()
    ok, tag = rfid.read_id()
    assert ok
    assert tag is not None
    if tag != bluefob:
        log.warn("read tag " + str(tag))
    else:
        log.yay("blue fob detected")
    pass


def relay_test():
    log.ok("testing relay..")
    relay = Relay()
    relay.set_pourer(2)
    abit = 0.05
    for i in range(5):
        relay.open()
        time.sleep(abit)
        relay.close()
        time.sleep(abit)


class FakeFM:
    def __init__(self):
        self.start = time.time()
        pass

    def reset(self):
        self.start = time.time()

    def enable(self):
        pass

    def disable(self):
        pass

    def poured_ccs(self):
        return int(time.time() - self.start)


def faucet_test():
    fm = FakeFM()
    relay_board = RelayBoard([
        ["water", 2],
        ["orange", 3],
    ], fm)
    faucet = Faucet(relay_board)
    r = parse_testrecipe("test_resources/orangejuice.yml")
    faucet.dispense(r)
    pass


def parse_testrecipe(file):
    r = Recipe()
    with open(file, "r") as stream:
        try:
            r.from_ymlfile(stream)
        except yaml.YAMLError as e:
            log.error("yaml error! couldnt parse " + file)
    return r


def recipes_test():
    try:
        r = parse_testrecipe("test_resources/malformed1.yml")
        r = parse_testrecipe("test_resources/malformed2.yml")
        r = parse_testrecipe("test_resources/malformed3.yml")
        r = parse_testrecipe("test_resources/malformed4.yml")
        r = parse_testrecipe("test_resources/malformed5.yml")
        r = parse_testrecipe("test_resources/orangejuice.yml")
        for tap, amount in r.steps:
            log.yay("{}[{}] - {}cc".format(tap, r.taps[tap], amount))

    except Exception as e:
        log.error("got exception " + str(e))
        return False
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--scale', help='perform scale test', action='store_true')
    parser.add_argument('--rfid', help='perform rfid test', action='store_true')
    parser.add_argument('--relay', help='perform relay board test', action='store_true')
    parser.add_argument('--allio', help='perform all sensors/io tests', action='store_true')
    parser.add_argument('--all', help='perform all tests', action='store_true')
    parser.add_argument('--core', help='perform core test', action='store_true')
parser.add_argument('--faucet', help='perform faucet test', action='store_true')
parser.add_argument('--recipes', help='perform recipes test', action='store_true')

args = parser.parse_args()
if len(sys.argv) == 1:
    args.all = True

if args.scale or args.all or args.allio:
    scale_test()
if args.rfid or args.all or args.allio:
    rfid_test()
if args.relay or args.all or args.allio:
    relay_test()
if args.faucet or args.all:
    faucet_test()
    if args.core or args.all:
        core_test()
if args.recipes or args.all:
    recipes_test()

    log.yay(">>>>>>>>>>> All good <<<<<<<<<<<<")

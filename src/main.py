#!/usr/bin/python3
import argparse

from RPi import GPIO

from core import log
from core.context import Context
from core.events import create_event, EventType, EventKey, json2evt, evt2json
from core.reactor import ReactorThread
from rfid.rfid import RfidThread


def main(args):
    log.loglevel = log.LVL_DBG

    context = Context(args)

    # todo delete
    from core.user import User
    giulio = User()
    giulio.name = "Giulio"
    giulio.tag = 797313096147
    giulio.glass.capacity = 250
    giulio.glass.weight = 280
    evt = create_event(EventType.REGISTRATION_REQUESTED)
    evt[EventKey.user] = giulio
    _, evt = json2evt(evt2json(evt))
    context.queue.put(evt)

    core_th = ReactorThread(context)
    rfid_th = RfidThread(context.queue)
    # gui_th = GuiThread(context.queue)

    try:
        core_th.start()
        rfid_th.start()
        # gui_th.start()

        core_th.join()
        rfid_th.running = False
        rfid_th.join()

    except KeyboardInterrupt:
        evt = create_event(EventType.SIGINT)
        context.queue.put(evt)

    # gui_th.running = False

    # gui_th.join()
    core_th.join()
    rfid_th.running = False
    rfid_th.join()
    GPIO.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", action="store", dest="host", help="Your AWS IoT custom endpoint")
    parser.add_argument("-r", "--rootCA", action="store", dest="rootCAPath", help="Root CA file path")
    parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
    parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")

    args = parser.parse_args()

    main(args)

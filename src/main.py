#!/usr/bin/env python3
import configparser
import os

from RPi import GPIO

from core import log
from core.context import Context
from core.events import create_event, EventType, EventKey, json2evt, evt2json
from core.reactor import ReactorThread
from core.recipe import parse_recipes_list_file
from core.user import parse_user_list_file
from dbg.tester_gui import TesterGui
from rfid.rfid import RfidThread

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def parse_users(ctx, file):
    ok, users = parse_user_list_file(file)
    if ok:
        log.ok("found " + str(len(users)) + " users")
        for user in users:
            evt = create_event(EventType.NEW_USER)
            evt[EventKey.user] = user
            _, evt = json2evt(evt2json(evt))
            ctx.queue.put(evt)


def parse_recipes(ctx, file):
    ok, recipes = parse_recipes_list_file(file)
    if ok:
        log.ok("found " + str(len(recipes)) + " recipes")
        for recipe in recipes:
            evt = create_event(EventType.NEW_RECIPE)
            evt[EventKey.add_recipe] = recipe
            _, evt = json2evt(evt2json(evt))
            ctx.queue.put(evt)


def main():

    conf = configparser.ConfigParser()
    conf.read("resources/config.ini")
    context = Context(conf)

    log.loglevel = log.logleveldict[conf["log"]["level"]]

    parse_users(context, conf["users"]["file"])
    parse_recipes(context, conf["recipes"]["file"])

    core_th = ReactorThread(context)
    rfid_th = RfidThread(context.queue)
    tester_th = TesterGui(context)

    try:
        core_th.start()
        rfid_th.start()
        tester_th.main()

        core_th.join()
        rfid_th.running = False
        rfid_th.join()

    except KeyboardInterrupt:
        evt = create_event(EventType.SIGINT)
        context.queue.put(evt)
        tester_th.destroy()

    core_th.join()
    rfid_th.running = False
    rfid_th.join()
    GPIO.cleanup()


if __name__ == "__main__":
    main()

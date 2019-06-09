#!/usr/bin/python3
import argparse

from RPi import GPIO

from core import log
from core.context import Context
from core.events import create_event, EventType, EventKey, json2evt, evt2json
from core.reactor import ReactorThread
from core.recipe import parse_recipes_list_file
from core.user import parse_user_list_file
from rfid.rfid import RfidThread


def parse_users(ctx):
    ok, users = parse_user_list_file("resources/users.yml")
    if ok:
        log.ok("found " + str(len(users)) + " users")
        for user in users:
            evt = create_event(EventType.NEW_USER)
            evt[EventKey.user] = user
            _, evt = json2evt(evt2json(evt))
            ctx.queue.put(evt)


def parse_recipes(ctx):
    ok, recipes = parse_recipes_list_file("resources/recipes.yml")
    if ok:
        log.ok("found " + str(len(recipes)) + " recipes")
        for recipe in recipes:
            evt = create_event(EventType.NEW_RECIPE)
            evt[EventKey.add_recipe] = recipe
            _, evt = json2evt(evt2json(evt))
            ctx.queue.put(evt)


def main(args):
    log.loglevel = log.LVL_DBG

    context = Context(args)

    parse_users(context)
    parse_recipes(context)

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

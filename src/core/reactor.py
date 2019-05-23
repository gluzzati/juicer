from core.event_handlers import *
from core.events import too_old
from core.state_callbacks import *


def get_evt(ctx):
    evt = ctx.queue.get(True)

    if not isinstance(evt, dict):
        log.error("not an event (" + str(type(evt)) + ")")
        return False, None

    if evt[EventKey.type] == EventType.SIGINT:
        ctx.running = False
        return False, None

    return True, evt


class Reactor:
    def __init__(self, context):
        self.ctx = context
        self.ctx.running = True
        self.handlers = dict()
        self.callbacks = dict()

        self.add_handler(EventType.RFID_DETECTED, rfid_detected_handler)
        self.add_handler(EventType.RFID_REMOVED, rfid_removed_handler)
        self.add_handler(EventType.REGISTRATION_REQUESTED, registration_requested_handler)
        self.add_handler(EventType.AUTO_WATEROFF, auto_wateroff_handler)
        self.add_handler(EventType.POUR_REQUESTED, pour_requested_handler)

        self.add_statecallback(Context.State.IDLE, on_idle)
        self.add_statecallback(Context.State.GLASS_ON, on_glass_on)
        self.add_statecallback(Context.State.POURING, on_pouring)

    def add_handler(self, evt_type, handler):
        self.handlers[evt_type] = handler

    def add_statecallback(self, state, callback):
        self.callbacks[state] = callback

    def handle(self, evt):
        if evt[EventKey.type] in self.handlers:
            return self.handlers[evt[EventKey.type]](self.ctx, evt)
        else:
            log.error("unknown event " + evt[EventKey.type])
            return False, None

    def change_state(self, next_state):
        if next_state in self.callbacks:
            return self.callbacks[next_state](self.ctx)
        else:
            log.error("unknown state " + str(next_state))
            return False, None

    def run(self):
        while self.ctx.running:

            ok, evt = get_evt(self.ctx)

            if not ok or too_old(evt):
                continue

            ok, next_state = self.handle(evt)
            ok, res = self.change_state(next_state)

        return 0


class ReactorThread(Thread):
    def __init__(self, context):
        self.ctx = context
        super().__init__()

    def run(self):
        consumer = Reactor(self.ctx)
        consumer.run()
